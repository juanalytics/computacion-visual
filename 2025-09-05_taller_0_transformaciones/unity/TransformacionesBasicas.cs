using UnityEngine;

/// <summary>
/// Taller 0 - Transformaciones Básicas en Unity
/// Script que aplica transformaciones geométricas básicas a GameObjects
/// Autor: [Tu nombre]
/// Fecha: 2025-09-05
/// </summary>
public class TransformacionesBasicas : MonoBehaviour
{
    [Header("Configuración de Transformaciones")]
    [SerializeField] private float velocidadTraslacion = 2.0f;
    [SerializeField] private float velocidadRotacion = 50.0f;
    [SerializeField] private float velocidadEscala = 1.0f;
    [SerializeField] private float amplitudMovimiento = 3.0f;
    
    [Header("Tipo de Transformación")]
    [SerializeField] private TipoTransformacion tipoTransformacion = TipoTransformacion.Traslacion;
    
    [Header("Configuración Específica")]
    [SerializeField] private bool usarMovimientoSenoidal = true;
    [SerializeField] private bool aplicarEnX = true;
    [SerializeField] private bool aplicarEnY = true;
    [SerializeField] private bool aplicarEnZ = true;
    
    // Variables privadas
    private Vector3 posicionInicial;
    private Vector3 rotacionInicial;
    private Vector3 escalaInicial;
    private float tiempoTranscurrido = 0f;
    
    // Enum para tipos de transformación
    public enum TipoTransformacion
    {
        Traslacion,
        Rotacion,
        Escala,
        Compuesta
    }
    
    void Start()
    {
        // Guardar valores iniciales
        posicionInicial = transform.position;
        rotacionInicial = transform.eulerAngles;
        escalaInicial = transform.localScale;
        
        Debug.Log($"=== Transformaciones Básicas Iniciadas ===");
        Debug.Log($"Objeto: {gameObject.name}");
        Debug.Log($"Tipo: {tipoTransformacion}");
        Debug.Log($"Posición inicial: {posicionInicial}");
    }
    
    void Update()
    {
        // Incrementar tiempo
        tiempoTranscurrido += Time.deltaTime;
        
        // Aplicar transformación según el tipo seleccionado
        switch (tipoTransformacion)
        {
            case TipoTransformacion.Traslacion:
                AplicarTraslacion();
                break;
                
            case TipoTransformacion.Rotacion:
                AplicarRotacion();
                break;
                
            case TipoTransformacion.Escala:
                AplicarEscala();
                break;
                
            case TipoTransformacion.Compuesta:
                AplicarTransformacionCompuesta();
                break;
        }
    }
    
    /// <summary>
    /// Aplica traslación senoidal o lineal
    /// </summary>
    private void AplicarTraslacion()
    {
        Vector3 nuevaPosicion = posicionInicial;
        
        if (usarMovimientoSenoidal)
        {
            // Movimiento senoidal suave
            if (aplicarEnX)
                nuevaPosicion.x += Mathf.Sin(tiempoTranscurrido * velocidadTraslacion) * amplitudMovimiento;
            
            if (aplicarEnY)
                nuevaPosicion.y += Mathf.Cos(tiempoTranscurrido * velocidadTraslacion * 1.5f) * amplitudMovimiento * 0.5f;
            
            if (aplicarEnZ)
                nuevaPosicion.z += Mathf.Sin(tiempoTranscurrido * velocidadTraslacion * 0.8f) * amplitudMovimiento * 0.7f;
        }
        else
        {
            // Movimiento lineal alternante
            float movimiento = Mathf.PingPong(tiempoTranscurrido * velocidadTraslacion, amplitudMovimiento * 2) - amplitudMovimiento;
            
            if (aplicarEnX) nuevaPosicion.x += movimiento;
            if (aplicarEnY) nuevaPosicion.y += movimiento * 0.5f;
            if (aplicarEnZ) nuevaPosicion.z += movimiento * 0.7f;
        }
        
        transform.position = nuevaPosicion;
    }
    
    /// <summary>
    /// Aplica rotación continua en los ejes especificados
    /// </summary>
    private void AplicarRotacion()
    {
        Vector3 rotacion = Vector3.zero;
        
        if (aplicarEnX)
            rotacion.x = velocidadRotacion * Time.deltaTime;
        
        if (aplicarEnY)
            rotacion.y = velocidadRotacion * Time.deltaTime * 1.5f;
        
        if (aplicarEnZ)
            rotacion.z = velocidadRotacion * Time.deltaTime * 0.8f;
        
        // Usar Rotate para rotación incremental
        transform.Rotate(rotacion);
    }
    
    /// <summary>
    /// Aplica escalado oscilante usando función senoidal
    /// </summary>
    private void AplicarEscala()
    {
        Vector3 nuevaEscala = escalaInicial;
        
        float factorEscala = 1.0f + Mathf.Sin(tiempoTranscurrido * velocidadEscala * 2.0f) * 0.5f;
        
        if (aplicarEnX) nuevaEscala.x *= factorEscala;
        if (aplicarEnY) nuevaEscala.y *= factorEscala;
        if (aplicarEnZ) nuevaEscala.z *= factorEscala;
        
        transform.localScale = nuevaEscala;
    }
    
    /// <summary>
    /// Aplica múltiples transformaciones simultáneamente
    /// </summary>
    private void AplicarTransformacionCompuesta()
    {
        // 1. Traslación circular
        Vector3 nuevaPosicion = posicionInicial;
        float radio = amplitudMovimiento;
        nuevaPosicion.x += Mathf.Cos(tiempoTranscurrido * velocidadTraslacion) * radio;
        nuevaPosicion.z += Mathf.Sin(tiempoTranscurrido * velocidadTraslacion) * radio;
        nuevaPosicion.y += Mathf.Sin(tiempoTranscurrido * velocidadTraslacion * 2.0f) * radio * 0.3f;
        
        transform.position = nuevaPosicion;
        
        // 2. Rotación continua
        Vector3 rotacion = new Vector3(
            velocidadRotacion * Time.deltaTime * 1.2f,
            velocidadRotacion * Time.deltaTime * 0.8f,
            velocidadRotacion * Time.deltaTime * 0.6f
        );
        
        transform.Rotate(rotacion);
        
        // 3. Escala variable
        float factorEscala = 1.0f + Mathf.Sin(tiempoTranscurrido * velocidadEscala * 3.0f) * 0.3f;
        Vector3 nuevaEscala = escalaInicial * factorEscala;
        
        transform.localScale = nuevaEscala;
    }
    
    /// <summary>
    /// Reinicia las transformaciones a los valores iniciales
    /// </summary>
    public void ReiniciarTransformaciones()
    {
        transform.position = posicionInicial;
        transform.eulerAngles = rotacionInicial;
        transform.localScale = escalaInicial;
        tiempoTranscurrido = 0f;
        
        Debug.Log("Transformaciones reiniciadas");
    }
    
    /// <summary>
    /// Cambia el tipo de transformación en tiempo de ejecución
    /// </summary>
    public void CambiarTipoTransformacion(TipoTransformacion nuevoTipo)
    {
        tipoTransformacion = nuevoTipo;
        ReiniciarTransformaciones();
        
        Debug.Log($"Tipo de transformación cambiado a: {nuevoTipo}");
    }
    
    // Métodos para controles de UI
    public void SetVelocidadTraslacion(float velocidad) => velocidadTraslacion = velocidad;
    public void SetVelocidadRotacion(float velocidad) => velocidadRotacion = velocidad;
    public void SetVelocidadEscala(float velocidad) => velocidadEscala = velocidad;
    public void SetAmplitudMovimiento(float amplitud) => amplitudMovimiento = amplitud;
    
    // Información de debug en el inspector
    void OnDrawGizmos()
    {
        if (Application.isPlaying)
        {
            // Dibujar la posición inicial
            Gizmos.color = Color.yellow;
            Gizmos.DrawWireSphere(posicionInicial, 0.2f);
            
            // Dibujar trayectoria para traslación
            if (tipoTransformacion == TipoTransformacion.Traslacion || tipoTransformacion == TipoTransformacion.Compuesta)
            {
                Gizmos.color = Color.cyan;
                Gizmos.DrawLine(posicionInicial, transform.position);
            }
        }
    }
}
