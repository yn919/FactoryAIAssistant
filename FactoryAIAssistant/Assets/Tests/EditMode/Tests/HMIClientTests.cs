using FactoryAIAssistant.Client;
using NUnit.Framework;
using UnityEngine;
using TMPro;
using UnityEngine.UI;

namespace Tests.EditMode.Tests
{
    public class HMIClientTests
    {
        private HMIClient hmiClient;
        private GameObject hmiClientGameObject;

        [SetUp]
        public void Setup()
        {
            hmiClientGameObject = new GameObject("HMIClient");
            hmiClient = hmiClientGameObject.AddComponent<HMIClient>();

            // モック UI のセットアップ
            hmiClient.inputField = new GameObject("InputField").AddComponent<TMP_InputField>();
            hmiClient.chatContent = new GameObject("ChatContent").transform;
            hmiClient.userMessagePrefab = CreateMessagePrefab();
            hmiClient.aiMessagePrefab = CreateMessagePrefab();
            hmiClient.tempText = new GameObject("TempText").AddComponent<TextMeshProUGUI>();
            hmiClient.pressureText = new GameObject("PressureText").AddComponent<TextMeshProUGUI>();
            hmiClient.vibrationText = new GameObject("VibrationText").AddComponent<TextMeshProUGUI>();
            hmiClient.statusText = new GameObject("StatusText").AddComponent<TextMeshProUGUI>();
            hmiClient.scrollRect = new GameObject("ScrollRect").AddComponent<ScrollRect>();
        }

        private GameObject CreateMessagePrefab()
        {
            var go = new GameObject("MessagePrefab");
            go.AddComponent<TextMeshProUGUI>();
            return go;
        }

        [TearDown]
        public void Teardown()
        {
            Object.DestroyImmediate(hmiClientGameObject);
        }

        // OnAskButton の正常系（メッセージが空でない）
        [Test]
        public void OnAskButton_MessageNotEmpty_AddsUserMessage()
        {
            hmiClient.inputField.text = "テストメッセージ";

            hmiClient.OnAskButton();

            Assert.IsEmpty(hmiClient.inputField.text);
            Assert.AreEqual(1, hmiClient.chatContent.childCount);

            var msg = hmiClient.chatContent.GetChild(0).GetComponentInChildren<TextMeshProUGUI>();
            Assert.AreEqual("テストメッセージ", msg.text);
        }

        // OnAskButton の異常系（メッセージが空）
        [Test]
        public void OnAskButton_MessageEmpty_DoesNotAddMessage()
        {
            hmiClient.inputField.text = "";

            hmiClient.OnAskButton();

            Assert.AreEqual(0, hmiClient.chatContent.childCount);
        }
    }
}
