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

            var messageText = msgObj.GetComponentInChildren<TMP_Text>();
            if (messageText != null)
                messageText.text = message;

            var rect = msgObj.GetComponent<RectTransform>();
            var bubble = msgObj.transform.Find("Bubble");
            var contentRect = chatContent as RectTransform;

            LayoutRebuilder.ForceRebuildLayoutImmediate(rect);
            LayoutRebuilder.ForceRebuildLayoutImmediate(contentRect);

            float bubbleWidth = 0f;
            float bubbleHeight = 0f;

            if (bubble != null)
            {
                var bubbleLayout = bubble.GetComponent<LayoutElement>();
                var bubbleText = bubble.GetComponentInChildren<TMP_Text>();

                if (bubbleLayout != null && bubbleText != null)
                {
                    float paddingHorizontal = 24f;
                    float computedWidth = bubbleText.preferredWidth + paddingHorizontal;
                    float clampedWidth = Mathf.Clamp(computedWidth, 0f, 700f);
                    bubbleLayout.preferredWidth = clampedWidth;
                    bubbleWidth = clampedWidth;

                    LayoutRebuilder.ForceRebuildLayoutImmediate(bubbleText.rectTransform);
                    float paddingVertical = 16f;
                    float computedHeight = bubbleText.preferredHeight + paddingVertical;
                    bubbleLayout.preferredHeight = computedHeight;
                    bubbleLayout.minHeight = computedHeight;
                    bubbleLayout.flexibleHeight = 0f;
                    bubbleHeight = computedHeight;
                }
            }

            float yOffset = 0f;
            if (chatContent.childCount > 1)
            {
                var prevMsg = chatContent.GetChild(chatContent.childCount - 2) as RectTransform;
                yOffset = prevMsg.anchoredPosition.y - prevMsg.rect.height - 10f; // spacing
            }
            else
            {
                yOffset = 0f;
            }

            rect.anchoredPosition = new Vector2(0f, yOffset);
            rect.sizeDelta = new Vector2(bubbleWidth, bubbleHeight);

            float parentWidth = contentRect.rect.width;
            if (parentWidth > 0f && bubbleWidth > parentWidth - 32f)
            {
                bubbleWidth = Mathf.Max(0f, parentWidth - 32f);
                rect.sizeDelta = new Vector2(bubbleWidth, bubbleHeight);
            }

            Canvas.ForceUpdateCanvases();
            scrollRect.verticalNormalizedPosition = 0f;
        }
    }
}
