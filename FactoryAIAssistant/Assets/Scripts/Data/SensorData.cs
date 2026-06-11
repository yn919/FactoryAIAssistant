using System;

namespace FactoryAIAssistant.Data
{
    // Class representing sensor data received from the backend
    [Serializable]
    public class SensorData
    {
        public float temperature;
        public float pressure;
        public float vibration;
        public string status;
    }
}