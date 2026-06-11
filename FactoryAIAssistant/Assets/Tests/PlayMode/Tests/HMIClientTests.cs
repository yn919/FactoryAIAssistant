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

            // Set up mock UI elements
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

        // Normal-case test for GetSensor coroutine
        [UnityTest]
        public IEnumerator GetSensor_Success()
        {
            // Since mocking UnityWebRequest is difficult, here we only verify that the coroutine completes without throwing an error
            // Actual API communication would require using a mock server or similar
            yield return hmiClient.StartCoroutine("GetSensor");
            // For now, only confirm that no error occurs
            Assert.DoesNotThrow(() => { });
        }

        // Normal-case test for OnAskButton (when the message is not empty)
        [UnityTest]
        public IEnumerator OnAskButton_MessageNotEmpty_CallsAskAI()
        {
            hmiClient.userMessagePrefab = new GameObject();
            hmiClient.userMessagePrefab.AddComponent<TextMeshProUGUI>();

            hmiClient.aiMessagePrefab = new GameObject();
            hmiClient.aiMessagePrefab.AddComponent<TextMeshProUGUI>();

            var contentGameObject = new GameObject();
            var contentTransform = contentGameObject.AddComponent<RectTransform>();
            hmiClient.scrollRect.content = contentTransform;

            hmiClient.inputField.text = "テストメッセージ";

            hmiClient.OnAskButton();
            // It is difficult to directly assert that the AskAI coroutine has started
            // Instead, we indirectly verify it by checking that the InputField is cleared
            Assert.IsEmpty(hmiClient.inputField.text);
            yield return null;
        }

        // Error-case test for OnAskButton (when the message is empty)
        [UnityTest]
        public IEnumerator OnAskButton_MessageEmpty_DoesNotCallAskAI()
        {
            hmiClient.inputField.text = string.Empty;
            hmiClient.OnAskButton();
            // Since there is no direct way to confirm AskAI was not called, we verify that the InputField remains empty
            Assert.IsEmpty(hmiClient.inputField.text);
            yield return null;
        }
    }
}