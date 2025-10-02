using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Controlador principal de la escena de transformaciones
/// Maneja múltiples objetos con diferentes transformaciones
/// </summary>
public class ControladorEscena : MonoBehaviour
{
    [Header("Referencias de GameObjects")]
    [SerializeField] private GameObject cuboPrefab;
    [SerializeField] private GameObject esferaPrefab;
    [SerializeField] private GameObject cilindro;
    [SerializeField] private GameObject capsula;
    
    [Header("UI Controls")]
    [SerializeField] private Button botonReiniciar;
    [SerializeField] private Slider sliderVelocidad;
    [SerializeField] private Text textoInfo;
    
    // Referencias a los objetos creados
    private GameObject cuboTraslacion;
    private GameObject esferaRotacion;
    private GameObject cilindroEscala;
    private GameObject capsulaCompuesta;
    
    // Scripts de transformación
    private TransformacionesBasicas[] scriptTransformaciones;
    
    void Start()
    {
        CrearObjetosDemo();
        ConfigurarUI();
        
        Debug.Log("=== Escena de Transformaciones Iniciada ===");
        Debug.log("Objetos creados con diferentes tipos de transformación");
    }
    
    /// <summary>
    /// Crea los objetos de demostración con diferentes transformaciones
    /// </summary>
    private void CrearObjetosDemo()
    {
        // 1. Cubo con traslación senoidal
        cuboTraslacion = CrearObjeto("Cubo_Traslacion", PrimitiveType.Cube, new Vector3(-3, 0, 0), Color.red);
        var scriptCubo = cuboTraslacion.AddComponent<TransformacionesBasicas>();
        ConfigurarScript(scriptCubo, TransformacionesBasicas.TipoTransformacion.Traslacion, 2.0f, 50.0f, 1.0f, 2.0f);
        
        // 2. Esfera con rotación continua
        esferaRotacion = CrearObjeto("Esfera_Rotacion", PrimitiveType.Sphere, new Vector3(-1, 0, 0), Color.green);
        var scriptEsfera = esferaRotacion.AddComponent<TransformacionesBasicas>();
        ConfigurarScript(scriptEsfera, TransformacionesBasicas.TipoTransformacion.Rotacion, 1.0f, 90.0f, 1.0f, 1.0f);
        
        // 3. Cilindro con escala oscilante
        cilindroEscala = CrearObjeto("Cilindro_Escala", PrimitiveType.Cylinder, new Vector3(1, 0, 0), Color.blue);
        var scriptCilindro = cilindroEscala.AddComponent<TransformacionesBasicas>();
        ConfigurarScript(scriptCilindro, TransformacionesBasicas.TipoTransformacion.Escala, 1.0f, 30.0f, 2.0f, 1.5f);
        
        // 4. Cápsula con transformación compuesta
        capsulaCompuesta = CrearObjeto("Capsula_Compuesta", PrimitiveType.Capsule, new Vector3(3, 0, 0), Color.yellow);
        var scriptCapsula = capsulaCompuesta.AddComponent<TransformacionesBasicas>();
        ConfigurarScript(scriptCapsula, TransformacionesBasicas.TipoTransformacion.Compuesta, 1.5f, 60.0f, 1.5f, 2.5f);
        
        // Guardar referencias a todos los scripts
        scriptTransformaciones = new TransformacionesBasicas[] { scriptCubo, scriptEsfera, scriptCilindro, scriptCapsula };
    }
    
    /// <summary>
    /// Crea un objeto primitivo con material y posición específicos
    /// </summary>
    private GameObject CrearObjeto(string nombre, PrimitiveType tipo, Vector3 posicion, Color color)
    {
        GameObject obj = GameObject.CreatePrimitive(tipo);
        obj.name = nombre;
        obj.transform.position = posicion;
        
        // Configurar material
        Renderer renderer = obj.GetComponent<Renderer>();
        Material material = new Material(Shader.Find("Standard"));
        material.color = color;
        material.metallic = 0.3f;
        material.smoothness = 0.7f;
        renderer.material = material;
        
        return obj;
    }
    
    /// <summary>
    /// Configura un script de transformaciones con parámetros específicos
    /// </summary>
    private void ConfigurarScript(TransformacionesBasicas script, TransformacionesBasicas.TipoTransformacion tipo, 
                                 float velTraslacion, float velRotacion, float velEscala, float amplitud)
    {
        // Usar reflexión para configurar campos privados serializados
        var tipo_script = typeof(TransformacionesBasicas);
        
        var campoVelTraslacion = tipo_script.GetField("velocidadTraslacion", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
        var campoVelRotacion = tipo_script.GetField("velocidadRotacion", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
        var campoVelEscala = tipo_script.GetField("velocidadEscala", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
        var campoAmplitud = tipo_script.GetField("amplitudMovimiento", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
        var campoTipo = tipo_script.GetField("tipoTransformacion", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
        
        campoVelTraslacion?.SetValue(script, velTraslacion);
        campoVelRotacion?.SetValue(script, velRotacion);
        campoVelEscala?.SetValue(script, velEscala);
        campoAmplitud?.SetValue(script, amplitud);
        campoTipo?.SetValue(script, tipo);
    }
    
    /// <summary>
    /// Configura los elementos de UI
    /// </summary>
    private void ConfigurarUI()
    {
        if (botonReiniciar != null)
        {
            botonReiniciar.onClick.AddListener(ReiniciarTodasLasTransformaciones);
        }
        
        if (sliderVelocidad != null)
        {
            sliderVelocidad.value = 1.0f;
            sliderVelocidad.onValueChanged.AddListener(CambiarVelocidadGlobal);
        }
    }
    
    /// <summary>
    /// Reinicia todas las transformaciones
    /// </summary>
    public void ReiniciarTodasLasTransformaciones()
    {
        foreach (var script in scriptTransformaciones)
        {
            if (script != null)
            {
                script.ReiniciarTransformaciones();
            }
        }
        
        ActualizarTextoInfo("Todas las transformaciones reiniciadas");
    }
    
    /// <summary>
    /// Cambia la velocidad global de todas las animaciones
    /// </summary>
    public void CambiarVelocidadGlobal(float factor)
    {
        Time.timeScale = factor;
        ActualizarTextoInfo($"Velocidad global: {factor:F1}x");
    }
    
    /// <summary>
    /// Actualiza el texto informativo
    /// </summary>
    private void ActualizarTextoInfo(string mensaje)
    {
        if (textoInfo != null)
        {
            textoInfo.text = $"Transformaciones Básicas\n{mensaje}\nFPS: {(1.0f / Time.unscaledDeltaTime):F1}";
        }
    }
    
    void Update()
    {
        // Actualizar información cada segundo
        if (Time.time % 1.0f < Time.deltaTime)
        {
            ActualizarTextoInfo($"Tiempo: {Time.time:F1}s");
        }
        
        // Controles de teclado
        if (Input.GetKeyDown(KeyCode.R))
        {
            ReiniciarTodasLasTransformaciones();
        }
        
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Time.timeScale = Time.timeScale > 0 ? 0 : 1;
            ActualizarTextoInfo(Time.timeScale > 0 ? "Reanudado" : "Pausado");
        }
    }
}
