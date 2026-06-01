using System.Collections;
using System.Text;
using FactoryAIAssistant.Data;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;

namespace FactoryAIAssistant.Client
{
    // バックエンドとの通信を処理するクライアントクラス
    public class HMIClient : MonoBehaviour
    {
        private const string API_BASE = "https://localhost:5001";

        public TMP_InputField inputField;
        public TMP_Text chatLog;
        public TMP_Text tempText;
        public TMP_Text pressureText;
        public TMP_Text vibrationText;
        public TMP_Text statusText;

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

        private IEnumerator AskAI(string messeage)
        {
            chatLog.text += $"\n<color=cyan>YOU:</color> {messeage}\n";
            var json = JsonUtility.ToJson(new Question { message = messeage });

            using var request = UnityWebRequest.Put($"{API_BASE}/ask", "POST");
            var body = Encoding.UTF8.GetBytes(json);
            request.uploadHandler = new UploadHandlerRaw(body);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                var data = JsonUtility.FromJson<AnswerData>(request.downloadHandler.text);
                chatLog.text += $"<color=yellow>AI:</color> {data.message}\n";
            }
            else
            {
                chatLog.text += $"<color=red>Error: {request.error}</color>\n";
            }

            inputField.text = string.Empty;
        }
    }
}