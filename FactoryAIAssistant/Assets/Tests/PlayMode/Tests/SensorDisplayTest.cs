using System.Collections;
using NUnit.Framework;
using TMPro;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UI;

namespace FactoryAIAssistant.Client.Tests
{
    public class SensorDisplayTest
    {
        private GameObject _canvasGameObject;
        private SensorDisplay _sensorDisplay;
        private TextMeshProUGUI _tempText, _pressureText, _vibrationText;

        [SetUp]
        public void SetUp()
        {
            // Set up Canvas and Text objects
            _canvasGameObject = new GameObject("Canvas");
            _canvasGameObject.AddComponent<Canvas>();
            _canvasGameObject.AddComponent<CanvasScaler>();
            _canvasGameObject.AddComponent<GraphicRaycaster>();

            _tempText = CreateTextMeshProUGUI("TempText");
            _pressureText = CreateTextMeshProUGUI("PressureText");
            _vibrationText = CreateTextMeshProUGUI("VibrationText");

            // Set up SensorDisplay
            var sensorDisplayObject = new GameObject("SensorDisplay");
            _sensorDisplay = sensorDisplayObject.AddComponent<SensorDisplay>();
            _sensorDisplay.tempText = _tempText;
            _sensorDisplay.pressureText = _pressureText;
            _sensorDisplay.vibrationText = _vibrationText;

            // Explicitly call SensorDisplay's Start method (InvokeRepeating will begin)
            _sensorDisplay.SendMessage("Start");
        }

        [TearDown]
        public void TearDown()
        {
            Object.Destroy(_canvasGameObject);
            Object.Destroy(_sensorDisplay.gameObject);
        }

        private TextMeshProUGUI CreateTextMeshProUGUI(string name)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(TextMeshProUGUI));
            go.transform.SetParent(_canvasGameObject.transform);
            return go.GetComponent<TextMeshProUGUI>();
        }

        [UnityTest]
        public IEnumerator SensorDisplay_UpdatesTextAfterDelay()
        {
            // Arrange
            var initialTempText = _tempText.text;
            var initialPressureText = _pressureText.text;
            var initialVibrationText = _vibrationText.text;

            // Act
            yield return new WaitForSeconds(1.1f);
            
            // Assert
            // Verify that the text has been updated (should be different from initial values)
            Assert.AreNotEqual(initialTempText, _tempText.text);
            Assert.AreNotEqual(initialPressureText, _pressureText.text);
            Assert.AreNotEqual(initialVibrationText, _vibrationText.text);

            // Verify correct formatting
            StringAssert.Contains("温度 : ", _tempText.text);
            StringAssert.Contains(" ℃", _tempText.text);
            StringAssert.Contains("圧力 : ", _pressureText.text);
            StringAssert.Contains(" MPa", _pressureText.text);
            StringAssert.Contains("振動 : ", _vibrationText.text);
            StringAssert.Contains(" mm/s", _vibrationText.text);
        }

        [UnityTest]
        public IEnumerator SensorDisplay_TemperatureValueIsWithinRange()
        {
            yield return new WaitForSeconds(1.1f);
            var temp = ParseSensorValue(_tempText.text, "温度 : ", " ℃");
            Assert.That(temp, Is.InRange(60f, 85f));
        }

        [UnityTest]
        public IEnumerator SensorDisplay_PressureValueIsWithinRange()
        {
            yield return new WaitForSeconds(1.1f);
            var pressure = ParseSensorValue(_pressureText.text, "圧力 : ", " MPa");
            Assert.That(pressure, Is.InRange(1.8f, 2.5f));
        }

        [UnityTest]
        public IEnumerator SensorDisplay_VibrationValueIsWithinRange()
        {
            yield return new WaitForSeconds(1.1f);
            var vibration = ParseSensorValue(_vibrationText.text, "振動 : ", " mm/s");
            Assert.That(vibration, Is.InRange(0.1f, 0.8f));
        }

        private float ParseSensorValue(string text, string prefix, string suffix)
        {
            var valueString = text.Replace(prefix, "").Replace(suffix, "");
            return float.Parse(valueString);
        }
    }
}