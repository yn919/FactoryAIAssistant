using System.Collections;
using System.Text;
using FactoryAIAssistant.Data;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

namespace FactoryAIAssistant.Client
{
    // Client class that handles communication with the backend
    public class HMIClient : MonoBehaviour
    {
        private const string API_BASE = "http://localhost:8000";

        public TMP_InputField inputField;
        public Transform chatContent;
        public GameObject userMessagePrefab;
        public GameObject aiMessagePrefab;
        public TMP_Text tempText;
        public TMP_Text pressureText;
        public TMP_Text vibrationText;
        public TMP_Text statusText;
        public ScrollRect scrollRect;

        private void Start()
        {
            StartCoroutine(SensorLoop());
        }

        private IEnumerator SensorLoop()
        {
            while (true)
            {
                yield return GetSensor();
                yield return new WaitForSeconds(5f);
            }
        }

        private IEnumerator GetSensor()
        {
            using (var request = UnityWebRequest.Get($"{API_BASE}/sensor"))
            {
                yield return request.SendWebRequest();

                        var data = JsonUtility.FromJson<SensorData>(request.downloadHandler.text);
                        tempText.text = $"温度：{data.temperature:F1} ℃";
                        pressureText.text = $"圧力：{data.pressure:F2} MPa";
                        vibrationText.text = $"振動：{data.vibration:F2} mm/s";
                        statusText.text = data.status == "warning" ? "警告" : "正常";
                        statusText.color = data.status == "warning" ? Color.red : Color.green;
                    }
                }

        public void OnAskButton()
        {
            if (!string.IsNullOrEmpty(inputField.text)) StartCoroutine(AskAI(inputField.text));
        }

        private IEnumerator AskAI(string message)
        {
            AddMessage(message, true);
            inputField.text = string.Empty;

            var json = JsonUtility.ToJson(new Question { message = message });

            using (var request = new UnityWebRequest($"{API_BASE}/ask", "POST"))
            {
                var body = Encoding.UTF8.GetBytes(json);
                request.uploadHandler = new UploadHandlerRaw(body);
                request.downloadHandler = new DownloadHandlerBuffer();
                request.SetRequestHeader("Content-Type", "application/json");

                yield return request.SendWebRequest();

                if (request.result == UnityWebRequest.Result.Success)
                {
                    var data = JsonUtility.FromJson<AnswerData>(request.downloadHandler.text);
                    AddMessage(data.answer, false);
                }
                else
                {
                    AddMessage($"エラー：{request.error}", false);
                }
            }

            inputField.text = string.Empty;
        }

        private void AddMessage(string message, bool isMine)
        {
            var prefab = isMine ? userMessagePrefab : aiMessagePrefab;
            var msgObj = Instantiate(prefab, chatContent, false);
            var rect = msgObj.GetComponent<RectTransform>();
            // Reset transform but do not override prefab anchors which control layout
            rect.localPosition = Vector3.zero;
            rect.localScale = Vector3.one;
            rect.anchoredPosition = Vector2.zero;

            // Find the Bubble child and the MessageText explicitly to avoid picking other TMPs
            var bubble = msgObj.transform.Find("Bubble");

            TMP_Text messageText = null;
            if (bubble != null)
            {
                // prefer a child named MessageText under Bubble
                var msgTextTransform = bubble.Find("MessageText");
                if (msgTextTransform != null)
                {
                    messageText = msgTextTransform.GetComponent<TMP_Text>();
                }
            }
            // fallback to any TMP found under the row
            if (messageText == null)
            {
                messageText = msgObj.GetComponentInChildren<TMP_Text>();
            }

            if (messageText != null)
            {
                messageText.text = message;
            }

            // Ensure alignment via HorizontalLayoutGroup childAlignment and spacer flexible widths
            var hlg = msgObj.GetComponent<HorizontalLayoutGroup>();
            if (hlg != null)
            {
                hlg.childAlignment = isMine ? TextAnchor.MiddleRight : TextAnchor.MiddleLeft;
            }

            var leftSpacer = msgObj.transform.Find("LeftSpacer");
            var rightSpacer = msgObj.transform.Find("RightSpacer");
            if (leftSpacer != null && rightSpacer != null)
            {
                var leftLE = leftSpacer.GetComponent<LayoutElement>() ?? leftSpacer.gameObject.AddComponent<LayoutElement>();
                var rightLE = rightSpacer.GetComponent<LayoutElement>() ?? rightSpacer.gameObject.AddComponent<LayoutElement>();
                leftLE.preferredWidth = 0f;
                rightLE.preferredWidth = 0f;
                leftLE.flexibleWidth = isMine ? 1f : 0f;
                rightLE.flexibleWidth = isMine ? 0f : 1f;
            }

            // Adjust bubble width dynamically based on text preferred width, clamped to max
            if (bubble != null)
            {
                var bubbleLayout = bubble.GetComponent<LayoutElement>() ?? bubble.gameObject.AddComponent<LayoutElement>();
                // ensure ContentSizeFitter on bubble does not conflict at runtime
                var bubbleCSF = bubble.GetComponent<ContentSizeFitter>();
                if (bubbleCSF != null)
                {
                    // prefer PreferredSize for horizontal fit
                    bubbleCSF.horizontalFit = ContentSizeFitter.FitMode.PreferredSize;
                }

                // find TMP under bubble specifically
                var bubbleText = bubble.GetComponentInChildren<TMP_Text>();
                if (bubbleText != null)
                {
                    float padding = 24f; // left + right padding inside bubble
                    float computedWidth = bubbleText.preferredWidth + padding;
                    float clamped = Mathf.Clamp(computedWidth, 0f, 700f);
                    bubbleLayout.preferredWidth = clamped;
                    bubbleLayout.flexibleWidth = 0f;
                    bubbleLayout.minWidth = 0f;
                }

                // Ensure Bubble has a visible Image at runtime; if missing, assign Unity builtin UI sprite
                var img = bubble.GetComponent<Image>();
                if (img == null)
                {
                    img = bubble.gameObject.AddComponent<Image>();
                    img.color = isMine ? new Color32(0x5A, 0xC8, 0xFF, 0xFF) : new Color32(0x2E, 0x3A, 0x46, 0xFF);
                }
                if (img.sprite == null)
                {
                    // Try built-in resource first (may fail in some Unity versions)
                    Sprite builtinSprite = null;
                    try
                    {
                        builtinSprite = Resources.GetBuiltinResource<Sprite>("UI/Skin/UISprite.psd");
                    }
                    catch { builtinSprite = null; }

                    if (builtinSprite != null)
                    {
                        img.sprite = builtinSprite;
                        img.type = Image.Type.Sliced;
                    }
                    else
                    {
                        // Fallback: create a simple white 1x1 sprite so the Image is visible at runtime
                        var tex = Texture2D.whiteTexture;
                        img.sprite = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), new Vector2(0.5f, 0.5f));
                        img.type = Image.Type.Simple;
                    }
                }
            }

            // Force layout rebuild to apply alignment and sizes
            var contentRect = chatContent as RectTransform;
            if (contentRect != null)
            {
                LayoutRebuilder.ForceRebuildLayoutImmediate(contentRect);
            }
            LayoutRebuilder.ForceRebuildLayoutImmediate(rect);

            // Verify placement: if bubble is not near the expected side, perform manual anchor fallback
            var rowLayout = msgObj.GetComponent<HorizontalLayoutGroup>();
            var bubbleRect = bubble != null ? bubble.GetComponent<RectTransform>() : null;
            bool appliedManualFallback = false;
            if (bubbleRect != null)
            {
                // determine where bubble ended up (local position)
                float localX = bubbleRect.anchoredPosition.x;
                var bubbleLE = bubble.GetComponent<LayoutElement>();
                float bubbleWidth = bubbleLE != null && bubbleLE.preferredWidth > 0f ? bubbleLE.preferredWidth : bubbleRect.rect.width;
                var parentWidth = rect.rect.width;

                // Only apply manual fallback if the bubble spans nearly full width (layout failure),
                // or if bubble is centered and spacers offer no flexible width to push it left/right.
                bool spansNearlyFull = bubbleWidth >= parentWidth - 10f;

                // reuse spacers found earlier (do not redeclare variable names)
                leftSpacer = leftSpacer ?? msgObj.transform.Find("LeftSpacer");
                rightSpacer = rightSpacer ?? msgObj.transform.Find("RightSpacer");
                var leftLE = leftSpacer != null ? leftSpacer.GetComponent<LayoutElement>() : null;
                var rightLE = rightSpacer != null ? rightSpacer.GetComponent<LayoutElement>() : null;

                bool spacersAreInactive = (leftLE == null || leftLE.flexibleWidth <= 0f) && (rightLE == null || rightLE.flexibleWidth <= 0f);
                bool bubbleCentered = Mathf.Abs(localX) < 5f;

                bool shouldBeRight = isMine;
                bool incorrectlyPlaced = spansNearlyFull || (bubbleCentered && spacersAreInactive);

                if (incorrectlyPlaced)
                {
                    // disable automatic row layout to preserve manual placement
                    if (rowLayout != null) rowLayout.enabled = false;

                    float horizontalMargin = 8f;
                    float finalWidth = bubbleLE != null && bubbleLE.preferredWidth > 0f ? bubbleLE.preferredWidth : bubbleRect.sizeDelta.x;

                    if (shouldBeRight)
                    {
                        bubbleRect.anchorMin = new Vector2(1f, 0.5f);
                        bubbleRect.anchorMax = new Vector2(1f, 0.5f);
                        bubbleRect.pivot = new Vector2(1f, 0.5f);
                        bubbleRect.sizeDelta = new Vector2(finalWidth, bubbleRect.sizeDelta.y);
                        bubbleRect.anchoredPosition = new Vector2(-horizontalMargin, 0f);
                    }
                    else
                    {
                        bubbleRect.anchorMin = new Vector2(0f, 0.5f);
                        bubbleRect.anchorMax = new Vector2(0f, 0.5f);
                        bubbleRect.pivot = new Vector2(0f, 0.5f);
                        bubbleRect.sizeDelta = new Vector2(finalWidth, bubbleRect.sizeDelta.y);
                        bubbleRect.anchoredPosition = new Vector2(horizontalMargin, 0f);
                    }

                    appliedManualFallback = true;
                }
            }

            if (appliedManualFallback)
            {
                // provide richer debug info to help diagnose layout failures
                var leftLEForLog = leftSpacer != null ? leftSpacer.GetComponent<LayoutElement>() : null;
                var rightLEForLog = rightSpacer != null ? rightSpacer.GetComponent<LayoutElement>() : null;
                Debug.Log($"[HMIClient] Applied manual bubble placement (isMine={isMine}) message='{(messageText!=null?messageText.text:"(null)")}' parentW={rect.rect.width:F1} bubbleW={bubbleRect.rect.width:F1} leftFlex={(leftLEForLog!=null?leftLEForLog.flexibleWidth:-1):-1} rightFlex={(rightLEForLog!=null?rightLEForLog.flexibleWidth:-1):-1}");
            }

            Canvas.ForceUpdateCanvases();
            scrollRect.verticalNormalizedPosition = 0f;
        }
    }
}