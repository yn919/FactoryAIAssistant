// FactoryAIAssistant/Assets/Scripts/Data/ChatResponseData.cs
namespace FactoryAIAssistant.Data
{
    // バックエンドから受け取るチャットレスポンスデータを表すクラス
    [System.Serializable]
    public class ChatResponseData
    {
        public string responseMessage;
        public string sender;
        public string timestamp;
    }
}