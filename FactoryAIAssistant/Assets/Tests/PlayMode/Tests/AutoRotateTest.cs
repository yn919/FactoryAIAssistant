using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace FactoryAIAssistant.Client.Tests
{
    public class AutoRotateTest
    {
        [UnityTest]
        public IEnumerator AutoRotate_RotatesObjectOverTime()
        {
            // Arrange
            var testObject = new GameObject("TestRotateObject");
            var autoRotate = testObject.AddComponent<AutoRotate>();
            autoRotate.speed = 90f;

            var initialRotation = testObject.transform.rotation;

            // Act
            yield return new WaitForSeconds(1.0f);

            // Assert
            // Verify that the Y-axis has rotated by about 90 degrees after 1 second (with tolerance).
            var expectedRotationY = (initialRotation.eulerAngles.y + 90f) % 360f;
            Assert.That(testObject.transform.rotation.eulerAngles.y, Is.EqualTo(expectedRotationY).Within(0.5f));

            // Cleanup
            Object.Destroy(testObject);
        }
    }
}