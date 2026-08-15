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
            using var request = UnityWebRequest.Get($"{API_BASE}/sensor");
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
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

            using var request = UnityWebRequest.PostWwwForm($"{API_BASE}/ask", "");
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

            inputField.text = string.Empty;
        }

        private void AddMessage(string message, bool isMine)
        {
            var prefab = isMine ? userMessagePrefab : aiMessagePrefab;
            var msgObj = Instantiate(prefab, chatContent, false);
            var rect = msgObj.GetComponent<RectTransform>();
            rect.localPosition = Vector3.zero;
            rect.localScale = Vector3.one;
            rect.anchorMin = new Vector2(0f, 0f);
            rect.anchorMax = new Vector2(1f, 1f);
            rect.pivot = new Vector2(0.5f, 0.5f);
            rect.anchoredPosition = Vector2.zero;
            rect.sizeDelta = Vector2.zero;

            // Set message text
            var messageText = msgObj.GetComponentInChildren<TMP_Text>();
            messageText.text = message;

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
            var bubble = msgObj.transform.Find("Bubble");
            if (bubble != null)
            {
                var bubbleLayout = bubble.GetComponent<LayoutElement>() ?? bubble.gameObject.AddComponent<LayoutElement>();
                var bubbleText = bubble.GetComponentInChildren<TMP_Text>();
                if (bubbleText != null)
                {
                    float padding = 24f; // left + right padding inside bubble
                    float computedWidth = bubbleText.preferredWidth + padding;
                    bubbleLayout.preferredWidth = Mathf.Clamp(computedWidth, 0f, 700f);
                    bubbleLayout.flexibleWidth = 0f;
                    bubbleLayout.minWidth = 0f;
                }
            }

            // Force layout rebuild to apply alignment and sizes
            var contentRect = chatContent as RectTransform;
            if (contentRect != null)
            {
                LayoutRebuilder.ForceRebuildLayoutImmediate(contentRect);
            }
            LayoutRebuilder.ForceRebuildLayoutImmediate(rect);

            // Fallback: if layout doesn't place bubble correctly on some devices/configs,
            // disable this row's HorizontalLayoutGroup and position Bubble manually.
            var rowLayout = msgObj.GetComponent<HorizontalLayoutGroup>();
            var bubbleRect = bubble != null ? bubble.GetComponent<RectTransform>() : null;
            if (bubbleRect != null)
            {
                // compute target size for bubble based on LayoutElement if present
                var bubbleLayout = bubble.GetComponent<LayoutElement>();
                float finalWidth = bubbleLayout != null && bubbleLayout.preferredWidth > 0f ? bubbleLayout.preferredWidth : bubbleRect.sizeDelta.x;
                // disable automatic row layout to preserve manual placement
                if (rowLayout != null) rowLayout.enabled = false;

                // anchor and place bubble at left or right inside the row
                float horizontalMargin = 8f;
                if (isMine)
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
            }

            Canvas.ForceUpdateCanvases();
            scrollRect.verticalNormalizedPosition = 0f;
        }
    }
}