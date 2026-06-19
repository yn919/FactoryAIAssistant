using TMPro;
using UnityEngine;

public class SensorDisplay : MonoBehaviour
{
    public TMP_Text tempText;
    public TMP_Text pressureText;
    public TMP_Text vibrationText;

    private void Start()
    {
        InvokeRepeating(nameof(UpdateSensors), 0f, 1f);
    }

    private void UpdateSensors()
    {
        tempText.text = $"温度 : {Random.Range(60f, 85f):F1} ℃";
        pressureText.text = $"圧力 : {Random.Range(1.8f, 2.5f):F2} MPa";
        vibrationText.text = $"振動 : {Random.Range(0.1f, 0.8f):F2} mm/s";
    }
}