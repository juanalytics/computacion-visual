using UnityEngine;
using UnityEngine.UI;

public class CameraSwitcher : MonoBehaviour
{
    public Camera cam;
    public Slider fovSlider;
    public Slider sizeSlider;
    public Toggle orthoToggle;

    void Start()
    {
        if (fovSlider != null)
            fovSlider.onValueChanged.AddListener(UpdateFOV);

        if (sizeSlider != null)
            sizeSlider.onValueChanged.AddListener(UpdateSize);

        if (orthoToggle != null)
            orthoToggle.onValueChanged.AddListener(SetOrtho);
    }

    void UpdateFOV(float value)
    {
        if (cam != null && !cam.orthographic)
            cam.fieldOfView = value;
    }

    void UpdateSize(float value)
    {
        if (cam != null && cam.orthographic)
            cam.orthographicSize = value;
    }

    void SetOrtho(bool value)
    {
        if (cam != null)
            cam.orthographic = value;
    }
}
