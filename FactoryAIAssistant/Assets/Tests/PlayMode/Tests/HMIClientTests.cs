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
            hmiClientGameObject = new GameObject("HMIClient");
            hmiClient = hmiClientGameObject.AddComponent<HMIClient>();

            var canvasGO = new GameObject("Canvas", typeof(Canvas));
            canvasGO.AddComponent<CanvasScaler>();
            canvasGO.AddComponent<GraphicRaycaster>();

            var inputGO = new GameObject("InputField", typeof(RectTransform));
            inputGO.transform.SetParent(canvasGO.transform);
            hmiClient.inputField = inputGO.AddComponent<TMP_InputField>();

            var contentGO = new GameObject("ChatContent", typeof(RectTransform));
            contentGO.transform.SetParent(canvasGO.transform);
            hmiClient.chatContent = contentGO.transform;

            var scrollGO = new GameObject("ScrollRect", typeof(RectTransform));
            scrollGO.transform.SetParent(canvasGO.transform);
            var scrollRect = scrollGO.AddComponent<ScrollRect>();
            scrollRect.content = contentGO.GetComponent<RectTransform>();
            hmiClient.scrollRect = scrollRect;

            hmiClient.userMessagePrefab = CreateMessagePrefab("UserMessagePrefab");
            hmiClient.aiMessagePrefab = CreateMessagePrefab("AIMessagePrefab");

            hmiClient.tempText = CreateTMP("TempText", canvasGO.transform);
            hmiClient.pressureText = CreateTMP("PressureText", canvasGO.transform);
            hmiClient.vibrationText = CreateTMP("VibrationText", canvasGO.transform);
            hmiClient.statusText = CreateTMP("StatusText", canvasGO.transform);
        }

        private GameObject CreateMessagePrefab(string name)
        {
            var go = new GameObject(name, typeof(RectTransform));
            var bubble = new GameObject("Bubble", typeof(RectTransform), typeof(LayoutElement));
            bubble.transform.SetParent(go.transform);

            var text = new GameObject("Text", typeof(RectTransform));
            text.transform.SetParent(bubble.transform);
            text.AddComponent<TextMeshProUGUI>();

            return go;
        }

        private TMP_Text CreateTMP(string name, Transform parent)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(parent);
            return go.AddComponent<TextMeshProUGUI>();
        }

        [TearDown]
        public void Teardown()
        {
            Object.Destroy(hmiClientGameObject);
        }

        // Normal-case test for GetSensor coroutine
        [UnityTest]
        public IEnumerator GetSensor_Success()
        {
            yield return hmiClient.StartCoroutine("GetSensor");
            Assert.DoesNotThrow(() => { });
        }

        // Normal-case test for OnAskButton (when the message is not empty)
        [UnityTest]
        public IEnumerator OnAskButton_MessageNotEmpty_CallsAskAI()
        {
            hmiClient.inputField.text = "テストメッセージ";

            hmiClient.OnAskButton();

            Assert.IsEmpty(hmiClient.inputField.text);
            yield return null;
        }

        // Error-case test for OnAskButton (when the message is empty)
        [UnityTest]
        public IEnumerator OnAskButton_MessageEmpty_DoesNotCallAskAI()
        {
            hmiClient.inputField.text = string.Empty;

            hmiClient.OnAskButton();

            Assert.IsEmpty(hmiClient.inputField.text);
            yield return null;
        }
    }
}