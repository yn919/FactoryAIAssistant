using System.Collections;
using System.Text;
using FactoryAIAssistant.Data;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

namespace FactoryAIAssistant.Client
{
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

                if (request.result == UnityWebRequest.Result.Success && request.downloadHandler != null)
                {
                    var data = JsonUtility.FromJson<SensorData>(request.downloadHandler.text);
                    if (data != null)
                    {
                        if (tempText != null) tempText.text = $"温度：{data.temperature:F1} ℃";
                        if (pressureText != null) pressureText.text = $"圧力：{data.pressure:F2} MPa";
                        if (vibrationText != null) vibrationText.text = $"振動：{data.vibration:F2} mm/s";
                        if (statusText != null)
                        {
                            statusText.text = data.status == "warning" ? "警告" : "正常";
                            statusText.color = data.status == "warning" ? Color.red : Color.green;
                        }
                    }
                }
                else
                {
                    Debug.LogWarning($"[HMIClient] GetSensor request failed: {request.error}");
                }
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
            rect.localPosition = Vector3.zero;
            rect.localScale = Vector3.one;
            rect.anchoredPosition = Vector2.zero;

            var bubble = msgObj.transform.Find("Bubble");

            TMP_Text messageText = null;
            if (bubble != null)
            {
                var msgTextTransform = bubble.Find("MessageText");
                if (msgTextTransform != null)
                {
                    messageText = msgTextTransform.GetComponent<TMP_Text>();
                }
            }
            if (messageText == null)
            {
                messageText = msgObj.GetComponentInChildren<TMP_Text>();
            }

            if (messageText != null)
            {
                messageText.text = message;

                var msgRt = messageText.GetComponent<RectTransform>();
                if (msgRt != null)
                {
                    msgRt.anchorMin = new Vector2(0f, 0f);
                    msgRt.anchorMax = new Vector2(1f, 1f);
                    msgRt.offsetMin = new Vector2(8f, 0f);
                    msgRt.offsetMax = new Vector2(-8f, -8f);
                    msgRt.sizeDelta = Vector2.zero;
                }

                try { messageText.margin = new Vector4(8f, 6f, 8f, 6f); } catch { }

                var outline = messageText.GetComponent<Outline>();
                if (outline != null) outline.enabled = false;
                var shadow = messageText.GetComponent<Shadow>();
                if (shadow != null) shadow.enabled = false;
            }

            var hlg = msgObj.GetComponent<HorizontalLayoutGroup>();
            var rowLayout = hlg;
            if (hlg != null)
            {
                hlg.childAlignment = isMine ? TextAnchor.MiddleRight : TextAnchor.MiddleLeft;
            }

            var leftSpacer = msgObj.transform.Find("LeftSpacer");
            var rightSpacer = msgObj.transform.Find("RightSpacer");

            if (leftSpacer == null)
            {
                var go = new GameObject("LeftSpacer", typeof(RectTransform));
                go.transform.SetParent(msgObj.transform, false);
                leftSpacer = go.transform;
            }
            if (rightSpacer == null)
            {
                var go = new GameObject("RightSpacer", typeof(RectTransform));
                go.transform.SetParent(msgObj.transform, false);
                rightSpacer = go.transform;
            }

            var leftLEMain = leftSpacer.GetComponent<LayoutElement>() ?? leftSpacer.gameObject.AddComponent<LayoutElement>();
            var rightLEMain = rightSpacer.GetComponent<LayoutElement>() ?? rightSpacer.gameObject.AddComponent<LayoutElement>();
            leftLEMain.preferredWidth = 0f;
            rightLEMain.preferredWidth = 0f;
            leftLEMain.flexibleWidth = isMine ? 1f : 0f;
            rightLEMain.flexibleWidth = isMine ? 0f : 1f;

            if (bubble != null)
            {
                var bubbleLayout = bubble.GetComponent<LayoutElement>() ?? bubble.gameObject.AddComponent<LayoutElement>();

                var bubbleText = bubble.GetComponentInChildren<TMP_Text>();
                if (bubbleText != null)
                {
                    float padding = 24f;
                    float computedWidth = bubbleText.preferredWidth + padding;
                    float clamped = Mathf.Clamp(computedWidth, 0f, 700f);
                    bubbleLayout.preferredWidth = clamped;
                    bubbleLayout.flexibleWidth = 0f;
                    bubbleLayout.minWidth = 0f;
                }

                var img = bubble.GetComponent<Image>();
                if (img == null)
                {
                    img = bubble.gameObject.AddComponent<Image>();
                    img.color = isMine ? new Color32(0x5A, 0xC8, 0xFF, 0xFF) : new Color32(0x2E, 0x3A, 0x46, 0xFF);
                    img.type = Image.Type.Simple;
                }
            }

            var contentRect = chatContent as RectTransform;
            if (contentRect != null)
            {
                LayoutRebuilder.ForceRebuildLayoutImmediate(contentRect);
            }
            LayoutRebuilder.ForceRebuildLayoutImmediate(rect);

            if (bubble != null)
            {
                var bubbleLayout = bubble.GetComponent<LayoutElement>();
                var bubbleText = bubble.GetComponentInChildren<TMP_Text>();

                if (bubbleLayout != null && bubbleText != null)
                {
                    LayoutRebuilder.ForceRebuildLayoutImmediate(bubbleText.rectTransform);

                    float paddingVertical = 16f;
                    float computedHeight = bubbleText.preferredHeight + paddingVertical;

                    bubbleLayout.preferredHeight = computedHeight;
                    bubbleLayout.minHeight = computedHeight;
                    bubbleLayout.flexibleHeight = 0f;
                }
            }

            LayoutRebuilder.ForceRebuildLayoutImmediate(rect);

            if (bubble != null)
            {
                var bubbleLayoutAfter = bubble.GetComponent<LayoutElement>();
                var bubbleRectAfter = bubble.GetComponent<RectTransform>();
                if (bubbleLayoutAfter != null && bubbleRectAfter != null)
                {
                    float parentWidthAfter = rect.rect.width;
                    if (parentWidthAfter > 0f && bubbleLayoutAfter.preferredWidth > parentWidthAfter - 32f)
                    {
                        bubbleLayoutAfter.preferredWidth = Mathf.Max(0f, parentWidthAfter - 32f);
                        if (contentRect != null)
                        {
                            LayoutRebuilder.ForceRebuildLayoutImmediate(contentRect);
                        }
                        LayoutRebuilder.ForceRebuildLayoutImmediate(rect);
                    }
                }

                if (hlg != null)
                {
                    hlg.childAlignment = isMine ? TextAnchor.MiddleRight : TextAnchor.MiddleLeft;
                }
                if (leftSpacer != null && rightSpacer != null)
                {
                    var leftLEFinal = leftSpacer.GetComponent<LayoutElement>();
                    var rightLEFinal = rightSpacer.GetComponent<LayoutElement>();
                    if (leftLEFinal != null && rightLEFinal != null)
                    {
                        leftLEFinal.flexibleWidth = isMine ? 1f : 0f;
                        rightLEFinal.flexibleWidth = isMine ? 0f : 1f;
                    }
                }

                if (contentRect != null)
                {
                    LayoutRebuilder.ForceRebuildLayoutImmediate(contentRect);
                }
                LayoutRebuilder.ForceRebuildLayoutImmediate(rect);

                var bubbleRectFinal = bubble.GetComponent<RectTransform>();
                if (bubbleRectFinal != null)
                {
                    float horizontalMargin = 8f;
                    bool shouldBeRight = isMine;
                    bool isCentered = Mathf.Abs(bubbleRectFinal.anchoredPosition.x) < 8f;
                    if (isCentered)
                    {
                        if (rowLayout != null) rowLayout.enabled = false;
                        float finalWidth = (bubble.GetComponent<LayoutElement>() != null && bubble.GetComponent<LayoutElement>().preferredWidth > 0f)
                            ? bubble.GetComponent<LayoutElement>().preferredWidth
                            : bubbleRectFinal.sizeDelta.x;

                        bubbleRectFinal.sizeDelta = new Vector2(finalWidth, bubbleRectFinal.sizeDelta.y);

                        if (shouldBeRight)
                        {
                            bubbleRectFinal.anchorMin = new Vector2(1f, 0.5f);
                            bubbleRectFinal.anchorMax = new Vector2(1f, 0.5f);
                            bubbleRectFinal.pivot = new Vector2(1f, 0.5f);
                            bubbleRectFinal.anchoredPosition = new Vector2(-horizontalMargin, 0f);
                        }
                        else
                        {
                            bubbleRectFinal.anchorMin = new Vector2(0f, 0.5f);
                            bubbleRectFinal.anchorMax = new Vector2(0f, 0.5f);
                            bubbleRectFinal.pivot = new Vector2(0f, 0.5f);
                            bubbleRectFinal.anchoredPosition = new Vector2(horizontalMargin, 0f);
                        }
                    }
                }
            }

            Canvas.ForceUpdateCanvases();
            scrollRect.verticalNormalizedPosition = 0f;
        }
    }
}
