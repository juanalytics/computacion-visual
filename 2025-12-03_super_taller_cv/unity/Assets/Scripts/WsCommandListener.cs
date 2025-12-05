using System;
using System.Text;
using System.Threading.Tasks;
using NativeWebSocket;
using UnityEngine;

[Serializable]
public class WsEnvelope
{
    public string type;
    public CommandPayload payload;
}

[Serializable]
public class CommandPayload
{
    public string action;
    public PayloadParams @params;
    public float confidence;
    public string source;
}

[Serializable]
public class PayloadParams
{
    public string color;
    public float intensity = 1f;
    public string pose;
}

public class WsCommandListener : MonoBehaviour
{
    [Header("Connection")]
    [SerializeField] private string websocketUrl = "ws://localhost:8000/ws";
    [SerializeField] private bool autoConnect = true;

    [Header("Scene Targets")]
    [SerializeField] private Renderer targetRenderer;
    [SerializeField] private Animator targetAnimator;
    [SerializeField] private Light sceneLight;
    [SerializeField] private Transform cameraRig;
    [SerializeField] private Transform cameraNear;
    [SerializeField] private Transform cameraFar;
    [SerializeField] private IKRigController ikController;
    [SerializeField] private FxController fxController;

    private WebSocket _websocket;
    private bool _cameraToggle;

    private async void Start()
    {
        if (autoConnect)
        {
            await ConnectWebSocket();
        }
    }

    private async Task ConnectWebSocket()
    {
        _websocket = new WebSocket(websocketUrl);

        _websocket.OnOpen += () =>
        {
            Debug.Log("[UnityWS] Connection opened");
            SendStatus("ready");
        };

        _websocket.OnError += (err) => Debug.LogError($"[UnityWS] {err}");

        _websocket.OnClose += (code) =>
        {
            Debug.LogWarning($"[UnityWS] Closed: {code}");
        };

        _websocket.OnMessage += OnMessageReceived;

        await _websocket.Connect();
    }

    private void OnMessageReceived(byte[] bytes)
    {
        var json = Encoding.UTF8.GetString(bytes);
        var envelope = JsonUtility.FromJson<WsEnvelope>(json);

        if (envelope?.type == "command" && envelope.payload != null)
        {
            ApplyAction(envelope.payload);
        }
    }

    private void ApplyAction(CommandPayload payload)
    {
        var action = payload.action ?? "unknown";
        switch (action)
        {
            case "change_material":
                ApplyColor(payload.@params?.color);
                break;
            case "trigger_animation":
                TriggerAnimation();
                break;
            case "switch_camera":
                ToggleCamera();
                break;
            case "toggle_light":
                ToggleLight(payload.@params?.intensity ?? 1f);
                break;
            case "set_ik_pose":
                ApplyIkPose(payload.@params?.pose);
                break;
            case "fx_pulse":
                TriggerFx(payload.@params?.color, payload.@params?.intensity ?? 1f);
                break;
            default:
                Debug.Log($"[UnityWS] Unknown action: {action}");
                break;
        }
    }

    private void ApplyColor(string colorHex)
    {
        if (targetRenderer == null) return;
        if (ColorUtility.TryParseHtmlString(colorHex ?? "#44CCFF", out var color))
        {
            targetRenderer.material.color = color;
        }
    }

    private void TriggerAnimation()
    {
        if (targetAnimator == null) return;
        targetAnimator.SetTrigger("react");
    }

    private void ToggleLight(float intensity)
    {
        if (sceneLight == null) return;
        sceneLight.intensity = sceneLight.intensity > 0.1f ? 0f : intensity;
    }

    private void ToggleCamera()
    {
        if (cameraRig == null || cameraNear == null || cameraFar == null) return;
        _cameraToggle = !_cameraToggle;
        var target = _cameraToggle ? cameraFar : cameraNear;
        cameraRig.position = target.position;
        cameraRig.rotation = target.rotation;
    }

    private void ApplyIkPose(string pose)
    {
        if (ikController == null) return;
        ikController.SetPose(pose == "reach" ? "reach" : "idle");
    }

    private void TriggerFx(string colorHex, float intensity)
    {
        if (fxController == null) return;
        if (!ColorUtility.TryParseHtmlString(colorHex ?? "#FF6A00", out var color))
        {
            color = Color.white;
        }
        fxController.PlayFx(color, intensity);
    }

    private async void SendStatus(string state)
    {
        if (_websocket == null || _websocket.State != WebSocketState.Open) return;
        var status = new
        {
            timestamp = DateTime.UtcNow.ToString("o"),
            module = "unity",
            type = "status",
            payload = new { state }
        };
        var json = JsonUtility.ToJson(status);
        await _websocket.SendText(json);
    }

#if !UNITY_WEBGL || UNITY_EDITOR
    private void Update()
    {
        _websocket?.DispatchMessageQueue();
    }
#endif

    private async void OnDestroy()
    {
        if (_websocket != null)
        {
            await _websocket.Close();
        }
    }
}

