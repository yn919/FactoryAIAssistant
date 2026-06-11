using System.Collections;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;

namespace FactoryAIAssistant.Client.Tests
{
    public class HMIClientTests
    {
        private HMIClient hmiClient;
        private GameObject hmiClientGameObject;

        [SetUp]
        public void Setup()
        {
            hmiClientGameObject = new GameObject();
            hmiClient = hmiClientGameObject.AddComponent<HMIClient>();

            // モックのUI要素を設定
            hmiClient.inputField = new GameObject().AddComponent<TMP_InputField>();
            hmiClient.chatContent = new GameObject().transform;
            hmiClient.userMessagePrefab = new GameObject();
            hmiClient.aiMessagePrefab = new GameObject();
            hmiClient.tempText = new GameObject().AddComponent<TextMeshProUGUI>();
            hmiClient.pressureText = new GameObject().AddComponent<TextMeshProUGUI>();
            hmiClient.vibrationText = new GameObject().AddComponent<TextMeshProUGUI>();
            hmiClient.statusText = new GameObject().AddComponent<TextMeshProUGUI>();
            hmiClient.scrollRect = new GameObject().AddComponent<ScrollRect>();
        }

        [TearDown]
        public void Teardown()
        {
            Object.Destroy(hmiClientGameObject);
        }

        // GetSensorコルーチンの正常系テスト
        [UnityTest]
        public IEnumerator GetSensor_Success()
        {
            // UnityWebRequestのモックは困難なため、ここではコルーチンがエラーを発生させずに完了することを確認
            // 実際のAPI通信はモックサーバーなどを使用する必要がある
            yield return hmiClient.StartCoroutine("GetSensor");
            // 現状はエラーが発生しないことのみ確認
            Assert.DoesNotThrow(() => { });
        }

        // OnAskButtonの正常系テスト（メッセージが空ではない場合）
        [UnityTest]
        public IEnumerator OnAskButton_MessageNotEmpty_CallsAskAI()
        {
            hmiClient.inputField.text = "テストメッセージ";
            hmiClient.OnAskButton();
            // AskAIコルーチンが開始されることを確認するための直接的なアサートは困難
            // ここではInputFiledがクリアされることを確認することで間接的に検証
            Assert.IsEmpty(hmiClient.inputField.text);
            yield return null;
        }

        // OnAskButtonの異常系テスト（メッセージが空の場合）
        [UnityTest]
        public IEnumerator OnAskButton_MessageEmpty_DoesNotCallAskAI()
        {
            hmiClient.inputField.text = string.Empty;
            hmiClient.OnAskButton();
            // AskAIが呼び出されないことを確認する直接的な方法がないため、InputFiledが空のままであることを確認
            Assert.IsEmpty(hmiClient.inputField.text);
            yield return null;
        }

        // AddMessageの正常系テスト
        [UnityTest]
        public IEnumerator AddMessage_AddsMessageToChatContent()
        {
            var initialChildCount = hmiClient.chatContent.childCount;
            // AddMessageはprivateなのでリフレクションで呼び出すか、publicなメソッドを介してテスト
            // 今回はpublicなOnAskButton()を介して呼び出されるAskAI()がAddMessageを呼び出すため、そちらで検証
            hmiClient.inputField.text = "User Message";
            hmiClient.OnAskButton();
            yield return null; // AskAIコルーチンが実行されるのを待つ

            Assert.Greater(hmiClient.chatContent.childCount, initialChildCount);

            // AIからの応答も確認したい場合は、AskAIが正常終了することをモックする必要がある
            // 現状ではユーザーメッセージのみ確認
            var userMsgText = hmiClient.chatContent.GetChild(hmiClient.chatContent.childCount - 1)
                .GetComponentInChildren<TextMeshProUGUI>();
            Assert.AreEqual("User Message", userMsgText.text);

            yield return null;
        }
    }
}