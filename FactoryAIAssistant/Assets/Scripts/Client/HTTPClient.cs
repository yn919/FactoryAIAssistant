// FactoryAIAssistant/Assets/Scripts/Client.cs
namespace FactoryAIAssistant.Client
{
    using System.Threading.Tasks;

    // バックエンドとの通信を処理するクライアントクラス
    public class HTTPClient
    {
        private readonly string backendUrl;

        public HTTPClient(string url)
        {
            backendUrl = url;
        }

        public async Task<ChatResponseData> SendChatMessage(string message)
        {
            // TODO: ここにメッセージ送信ロジックを実装します
            // InputFieldの内容をバックエンドに送信し、Geminiの返信を受信する
            // UnityWebRequestを使用する想定

            // 例:
            // var request = UnityWebRequest.Post(backendUrl + "/chat", message);
            // request.SetRequestHeader("Content-Type", "application/json");
            // await request.SendWebRequest();
            // if (request.result == UnityWebRequest.Result.Success)
            // {
            //     return JsonUtility.FromJson<ChatResponseData>(request.downloadHandler.text);
            // }
            // else
            // {
            //     Debug.LogError($"Error: {request.error}");
            //     return null;
            // }
            return null; // 仮の実装
        }
    }
}
