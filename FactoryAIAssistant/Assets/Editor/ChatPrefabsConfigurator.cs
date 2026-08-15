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
    private const int PreferredWidth = 700;
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
        // Configure anchors: minX=0, maxX=1, pivotY=1
        rt.anchorMin = new Vector2(0f, rt.anchorMin.y);
        rt.anchorMax = new Vector2(1f, rt.anchorMax.y == 0 ? 1f : rt.anchorMax.y);
        rt.pivot = new Vector2(rt.pivot.x, 1f);

        // HorizontalLayoutGroup on root
        var hlg = root.GetComponent<HorizontalLayoutGroup>();
        if (hlg == null) hlg = root.AddComponent<HorizontalLayoutGroup>();
        hlg.childAlignment = TextAnchor.MiddleCenter;
        hlg.childControlWidth = false;
        hlg.childControlHeight = false;
        hlg.childForceExpandWidth = false;
        hlg.spacing = 8;
        hlg.padding.left = 8;
        hlg.padding.right = 8;

        // ContentSizeFitter vertical preferred
        var csf = root.GetComponent<ContentSizeFitter>();
        if (csf == null) csf = root.AddComponent<ContentSizeFitter>();
        csf.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
        csf.horizontalFit = ContentSizeFitter.FitMode.Unconstrained;

        // Find or create LeftSpacer, Bubble, RightSpacer (in that order)
        var leftSpacer = EnsureChild(root, "LeftSpacer");
        var bubble = EnsureChild(root, "Bubble");
        var rightSpacer = EnsureChild(root, "RightSpacer");

        // Configure spacers
        var leftLE = GetOrAdd<LayoutElement>(leftSpacer);
        var rightLE = GetOrAdd<LayoutElement>(rightSpacer);
        // For user: left flexible = 1, right = 0 (bubble on right)
        // For AI: left = 0, right = 1 (bubble on left)
        leftLE.flexibleWidth = isUser ? 1f : 0f;
        rightLE.flexibleWidth = isUser ? 0f : 1f;

        // Bubble: ensure Image
        var img = bubble.GetComponent<Image>();
        if (img == null) img = bubble.AddComponent<Image>();
        // Assign builtin UI sprite so Color shows reliably
        var builtin = (Sprite)EditorGUIUtility.Load("UI/Skin/UISprite.psd");
        if (builtin != null) img.sprite = builtin;
        img.type = Image.Type.Sliced;
        img.color = isUser ? UserColor : AIColor;

        // Bubble LayoutElement
        var bubbleLE = GetOrAdd<LayoutElement>(bubble);
        bubbleLE.preferredWidth = PreferredWidth;
        bubbleLE.flexibleWidth = 0f;

        // Bubble ContentSizeFitter
        var bubbleCSF = bubble.GetComponent<ContentSizeFitter>();
        if (bubbleCSF == null) bubbleCSF = bubble.AddComponent<ContentSizeFitter>();
        bubbleCSF.horizontalFit = ContentSizeFitter.FitMode.Unconstrained;
        bubbleCSF.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

        // Ensure there is a TextMeshPro child; find existing TMP and move under bubble
        var existingTMP = root.GetComponentInChildren<TextMeshProUGUI>(true);
        if (existingTMP != null)
        {
            // If TMP is not already under bubble, reparent
            if (existingTMP.transform.parent != bubble.transform)
            {
                existingTMP.transform.SetParent(bubble.transform, false);
            }
            // Adjust rect transform to stretch
            var tmpRT = existingTMP.GetComponent<RectTransform>();
            tmpRT.anchorMin = new Vector2(0f, 0f);
            tmpRT.anchorMax = new Vector2(1f, 1f);
            tmpRT.offsetMin = new Vector2(12f, 8f); // left, bottom padding
            tmpRT.offsetMax = new Vector2(-12f, -8f); // right, top padding

            // TMP settings
            existingTMP.enableWordWrapping = true;
            existingTMP.enableAutoSizing = false;
            existingTMP.fontSize = 22;
            existingTMP.color = Color.white;
            existingTMP.alignment = isUser ? TextAlignmentOptions.Right : TextAlignmentOptions.Left;
        }
        else
        {
            // create a new TMP child
            var go = new GameObject("MessageText", typeof(RectTransform));
            go.transform.SetParent(bubble.transform, false);
            var rtChild = go.GetComponent<RectTransform>();
            rtChild.anchorMin = new Vector2(0f, 0f);
            rtChild.anchorMax = new Vector2(1f, 1f);
            rtChild.offsetMin = new Vector2(12f, 8f);
            rtChild.offsetMax = new Vector2(-12f, -8f);
            var tmp = go.AddComponent<TextMeshProUGUI>();
            tmp.text = "New Message";
            tmp.enableWordWrapping = true;
            tmp.enableAutoSizing = false;
            tmp.fontSize = 22;
            tmp.color = Color.white;
            tmp.alignment = isUser ? TextAlignmentOptions.Right : TextAlignmentOptions.Left;
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
