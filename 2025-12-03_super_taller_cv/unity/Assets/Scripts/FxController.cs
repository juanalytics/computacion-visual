using UnityEngine;

public class FxController : MonoBehaviour
{
    [SerializeField] private ParticleSystem particleSystem;
    [SerializeField] private Light accentLight;

    private ParticleSystem.MainModule _main;

    private void Awake()
    {
        if (particleSystem != null)
        {
            _main = particleSystem.main;
        }
    }

    public void PlayFx(Color color, float intensity)
    {
        if (particleSystem == null) return;
        _main.startColor = color;
        particleSystem.Play(true);

        if (accentLight != null)
        {
            accentLight.color = color;
            accentLight.intensity = intensity;
            CancelInvoke(nameof(ResetLight));
            Invoke(nameof(ResetLight), 0.4f);
        }
    }

    private void ResetLight()
    {
        if (accentLight != null)
        {
            accentLight.intensity = 0f;
        }
    }
}

