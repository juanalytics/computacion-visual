using UnityEngine;
using extOSC;

public class VoiceController : MonoBehaviour
{
    public OSCReceiver Receiver; // Receptor OSC
    public GameObject Cubo;      // Objeto a controlar

    private void Start()
    {
        // Vincular el evento OSC con nuestra función
        Receiver.Bind("/comando", OnReceiveCommand);
    }

    private void OnReceiveCommand(OSCMessage message)
    {
        string comando = message.Values[0].StringValue;
        Debug.Log("Comando recibido: " + comando);

        // Acciones según el comando
        if (comando == "gira")
        {
            Cubo.transform.Rotate(Vector3.up * 45);
        }
        else if (comando == "salta")
        {
            Cubo.transform.Translate(Vector3.up * 2);
        }
        else if (comando == "color")
        {
            Cubo.GetComponent<Renderer>().material.color = Random.ColorHSV();
        }
    }
}
