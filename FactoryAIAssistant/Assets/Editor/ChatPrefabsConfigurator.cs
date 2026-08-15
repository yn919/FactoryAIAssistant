using UnityEngine;
using UnityEditor;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using TMPro;

// Editor utility to configure chat message prefabs (UserMessage & AIAMessage)
// Adds HorizontalLayoutGroup / ContentSizeFitter on root, creates LeftSpacer/Bubble/RightSpacer,
// ensures Bubble has Image + LayoutElement + ContentSizeFitter, moves TMP_Text under Bubble,
// and sets colors / preferred width = 700px.
public static class ChatPrefabsConfigurator
{
    private const int MaxBubbleWidth = 700;
    private static readonly Color UserColor = new Color32(0x5A, 0xC8, 0xFF, 0xFF); // #5AC8FF
    private static readonly Color AIColor = new Color32(0x2E, 0x3A, 0x46, 0xFF);   // #2E3A46

    [MenuItem("Tools/Chat Prefab Configure/Apply to Prefabs")]
    public static void ApplyToPrefabs()
    {
        string[] prefabPaths = new string[]
        {
            "Assets/Prefabs/UserMessage.prefab",
            "Assets/Prefabs/AIAMessage.prefab"
        };

        foreach (var path in prefabPaths)
        {
            if (!System.IO.File.Exists(path))
            {
                Debug.LogWarning($"Prefab not found: {path}");
                continue;
            }

            var root = PrefabUtility.LoadPrefabContents(path);
            if (root == null)
            {
                Debug.LogWarning($"Failed to load prefab contents: {path}");
                continue;
            }

            ConfigurePrefab(root, path.Contains("UserMessage"));

            PrefabUtility.SaveAsPrefabAsset(root, path);
            PrefabUtility.UnloadPrefabContents(root);

            Debug.Log($"Configured prefab: {path}");
        }

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
    }

    private static void ConfigurePrefab(GameObject root, bool isUser)
    {
        // Ensure RectTransform exists
        var rt = root.GetComponent<RectTransform>();
        if (rt == null) rt = root.AddComponent<RectTransform>();
        rt.anchorMin = new Vector2(0f, 0f);
        rt.anchorMax = new Vector2(1f, 1f);
        rt.pivot = new Vector2(0.5f, 0.5f);
        rt.sizeDelta = Vector2.zero;

        // Layout row: full width, but bubble stays a fixed maximum width.
        var hlg = root.GetComponent<HorizontalLayoutGroup>();
        if (hlg == null) hlg = root.AddComponent<HorizontalLayoutGroup>();
        hlg.childAlignment = isUser ? TextAnchor.MiddleRight : TextAnchor.MiddleLeft;
        hlg.childControlWidth = false;
        hlg.childControlHeight = false;
        hlg.childForceExpandWidth = false;
        hlg.childForceExpandHeight = false;
        hlg.spacing = 8;
        hlg.padding.left = 8;
        hlg.padding.right = 8;

        var csf = root.GetComponent<ContentSizeFitter>();
        if (csf == null) csf = root.AddComponent<ContentSizeFitter>();
        csf.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
        csf.horizontalFit = ContentSizeFitter.FitMode.Unconstrained;

        // Find or create LeftSpacer, Bubble, RightSpacer (in that order)
        var leftSpacer = EnsureChild(root, "LeftSpacer");
        var bubble = EnsureChild(root, "Bubble");
        var rightSpacer = EnsureChild(root, "RightSpacer");

        // Configure spacers: the position is driven by the spacer width, not by the bubble transform itself.
        var leftLE = GetOrAdd<LayoutElement>(leftSpacer);
        var rightLE = GetOrAdd<LayoutElement>(rightSpacer);
        leftLE.preferredWidth = 0f;
        rightLE.preferredWidth = 0f;
        leftLE.flexibleWidth = isUser ? 1f : 0f;
        rightLE.flexibleWidth = isUser ? 0f : 1f;

        // Bubble: ensure Image
        var img = bubble.GetComponent<Image>();
        if (img == null) img = bubble.AddComponent<Image>();
        var builtin = (Sprite)EditorGUIUtility.Load("UI/Skin/UISprite.psd");
        if (builtin != null) img.sprite = builtin;
        img.type = Image.Type.Sliced;
        img.color = isUser ? UserColor : AIColor;

        // Ensure bubble has a RectTransform (do not force anchors here to avoid breaking existing layout)
        var bubbleRT = bubble.GetComponent<RectTransform>();
        if (bubbleRT == null) bubbleRT = bubble.AddComponent<RectTransform>();

        // Fix common typo in existing prefabs: "MessgeText" -> "MessageText"
        var misnamed = bubble.transform.parent != null ? bubble.transform.parent.Find("MessgeText") : null;
        if (misnamed != null)
        {
            misnamed.name = "MessageText";
        }

        // If a MessageText exists directly under Bubble but with wrong name, fix it
        var msgTextChild = bubble.transform.Find("MessgeText");
        if (msgTextChild != null)
        {
            msgTextChild.name = "MessageText";
        }

        // Ensure MessageText child exists (will be created below if missing)

        // Bubble LayoutElement: dynamic width by text content, capped at 700px.
        var bubbleLE = GetOrAdd<LayoutElement>(bubble);
        bubbleLE.preferredWidth = 0f;
        bubbleLE.flexibleWidth = 0f;
        bubbleLE.minWidth = 0f;
        bubbleLE.minHeight = 0f;

        // Bubble ContentSizeFitter
        var bubbleCSF = bubble.GetComponent<ContentSizeFitter>();
        if (bubbleCSF == null) bubbleCSF = bubble.AddComponent<ContentSizeFitter>();
        bubbleCSF.horizontalFit = ContentSizeFitter.FitMode.PreferredSize;
        bubbleCSF.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

        // Ensure there is a TextMeshPro child; find existing TMP and move under bubble.
        var existingMessageText = root.GetComponentInChildren<TextMeshProUGUI>(true);
        if (existingMessageText != null)
        {
            if (existingMessageText.transform.parent != bubble.transform)
            {
                existingMessageText.transform.SetParent(bubble.transform, false);
            }

            var messageRect = existingMessageText.GetComponent<RectTransform>();
            messageRect.anchorMin = new Vector2(0f, 0f);
            messageRect.anchorMax = new Vector2(1f, 1f);
            messageRect.offsetMin = new Vector2(12f, 8f);
            messageRect.offsetMax = new Vector2(-12f, -8f);
            messageRect.sizeDelta = Vector2.zero;

            existingMessageText.enableWordWrapping = true;
            existingMessageText.enableAutoSizing = false;
            existingMessageText.fontSize = 22;
            existingMessageText.color = Color.white;
            existingMessageText.alignment = isUser ? TextAlignmentOptions.Right : TextAlignmentOptions.Left;
            existingMessageText.raycastTarget = false;
            existingMessageText.overflowMode = TextOverflowModes.Overflow;
        }
        else
        {
            var go = new GameObject("MessageText", typeof(RectTransform));
            go.transform.SetParent(bubble.transform, false);
            var rtChild = go.GetComponent<RectTransform>();
            rtChild.anchorMin = new Vector2(0f, 0f);
            rtChild.anchorMax = new Vector2(1f, 1f);
            rtChild.offsetMin = new Vector2(12f, 8f);
            rtChild.offsetMax = new Vector2(-12f, -8f);
            rtChild.sizeDelta = Vector2.zero;

            var messageText = go.AddComponent<TextMeshProUGUI>();
            messageText.text = "New Message";
            messageText.enableWordWrapping = true;
            messageText.enableAutoSizing = false;
            messageText.fontSize = 22;
            messageText.color = Color.white;
            messageText.alignment = isUser ? TextAlignmentOptions.Right : TextAlignmentOptions.Left;
            messageText.raycastTarget = false;
            messageText.overflowMode = TextOverflowModes.Overflow;
            messageText.margin = new Vector4(12f, 8f, 12f, 8f);
        }

        // Ensure CanvasRenderer exists on bubble and TMP exists
        if (bubble.GetComponent<CanvasRenderer>() == null) bubble.AddComponent<CanvasRenderer>();

        // Remove any stray Layout components on root children except the ones we manage
        // (leave as-is to avoid destructive edits)
    }

    private static GameObject EnsureChild(GameObject parent, string name)
    {
        var t = parent.transform.Find(name);
        if (t != null) return t.gameObject;
        var go = new GameObject(name, typeof(RectTransform));
        go.transform.SetParent(parent.transform, false);
        return go;
    }

    private static T GetOrAdd<T>(GameObject go) where T : Component
    {
        var c = go.GetComponent<T>();
        if (c == null) c = go.AddComponent<T>();
        return c;
    }
}
