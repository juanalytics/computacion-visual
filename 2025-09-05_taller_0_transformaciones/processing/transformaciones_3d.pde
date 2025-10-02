/**
 * Taller 0 - Transformaciones Básicas en Processing
 * Implementación de transformaciones geométricas 3D
 * Autor: [Tu nombre]
 * Fecha: 2025-09-05
 */

// Variables globales para animación
float tiempo = 0;
float velocidadAnimacion = 0.02;

// Variables para control de cámara
float anguloX = 0;
float anguloY = 0;
float zoom = 1.0;

// Colores para los objetos
color colorCubo = color(255, 100, 100);      // Rojo
color colorEsfera = color(100, 255, 100);    // Verde
color colorCilindro = color(100, 100, 255);  // Azul
color colorCompuesto = color(255, 255, 100); // Amarillo

void setup() {
  size(1200, 800, P3D);
  
  // Configuración inicial
  println("=== Taller 0: Transformaciones Básicas en Processing ===");
  println("Controles:");
  println("- Mouse: Rotar cámara");
  println("- Rueda del mouse: Zoom");
  println("- Tecla 'r': Reiniciar animación");
  println("- Tecla 's': Guardar captura");
}

void draw() {
  // Fondo con gradiente
  background(20, 30, 50);
  
  // Configurar luces
  configurarLuces();
  
  // Configurar cámara
  configurarCamara();
  
  // Dibujar sistema de coordenadas
  dibujarEjes();
  
  // Dibujar grid de referencia
  dibujarGrid();
  
  // Aplicar transformaciones y dibujar objetos
  dibujarCuboTraslacion();
  dibujarEsferaRotacion();
  dibujarCilindroEscala();
  dibujarObjetoCompuesto();
  
  // Información en pantalla
  dibujarInformacion();
  
  // Incrementar tiempo
  tiempo += velocidadAnimacion;
}

void configurarLuces() {
  // Luz ambiental
  ambientLight(60, 60, 80);
  
  // Luz direccional principal
  directionalLight(200, 200, 255, -1, 0.5, -1);
  
  // Luz puntual
  pointLight(255, 200, 150, 200, -100, 200);
}

void configurarCamara() {
  // Aplicar transformaciones de cámara
  translate(width/2, height/2, 0);
  scale(zoom);
  rotateX(anguloX);
  rotateY(anguloY);
}

void dibujarEjes() {
  // Guardar estado de transformación
  pushMatrix();
  
  strokeWeight(3);
  
  // Eje X (rojo)
  stroke(255, 0, 0);
  line(0, 0, 0, 100, 0, 0);
  
  // Eje Y (verde)
  stroke(0, 255, 0);
  line(0, 0, 0, 0, 100, 0);
  
  // Eje Z (azul)
  stroke(0, 0, 255);
  line(0, 0, 0, 0, 0, 100);
  
  strokeWeight(1);
  
  // Restaurar estado
  popMatrix();
}

void dibujarGrid() {
  pushMatrix();
  
  stroke(80, 80, 120, 100);
  strokeWeight(1);
  
  // Grid en el plano XZ
  for (int i = -200; i <= 200; i += 20) {
    line(i, 0, -200, i, 0, 200);
    line(-200, 0, i, 200, 0, i);
  }
  
  popMatrix();
}

void dibujarCuboTraslacion() {
  pushMatrix();
  
  // Transformación: Traslación senoidal
  float x = 100 * sin(tiempo);
  float y = 50 * cos(tiempo * 1.5);
  float z = 30 * sin(tiempo * 0.8);
  
  translate(x, y, z);
  
  // Dibujar cubo
  fill(colorCubo);
  stroke(0);
  strokeWeight(1);
  box(40);
  
  // Etiqueta
  fill(255);
  textAlign(CENTER);
  text("Traslación", 0, -30, 0);
  
  popMatrix();
}

void dibujarEsferaRotacion() {
  pushMatrix();
  
  // Posición fija
  translate(-120, -80, 50);
  
  // Transformación: Rotación continua en múltiples ejes
  rotateX(tiempo * 0.5);
  rotateY(tiempo * 0.8);
  rotateZ(tiempo * 0.3);
  
  // Dibujar esfera
  fill(colorEsfera);
  stroke(0);
  strokeWeight(1);
  sphere(25);
  
  // Marcador para mostrar rotación
  fill(255, 0, 0);
  noStroke();
  pushMatrix();
  translate(25, 0, 0);
  sphere(5);
  popMatrix();
  
  // Etiqueta (fuera de las rotaciones)
  popMatrix();
  pushMatrix();
  translate(-120, -120, 50);
  fill(255);
  textAlign(CENTER);
  text("Rotación", 0, 0, 0);
  
  popMatrix();
}

void dibujarCilindroEscala() {
  pushMatrix();
  
  // Posición fija
  translate(120, 80, -30);
  
  // Transformación: Escala oscilante
  float escala = 1.0 + 0.5 * sin(tiempo * 2);
  scale(escala);
  
  // Dibujar cilindro (usando rotación de rectángulos)
  fill(colorCilindro);
  stroke(0);
  strokeWeight(1);
  
  rotateX(PI/2);
  
  // Crear cilindro con beginShape/endShape
  int lados = 12;
  float radio = 20;
  float altura = 60;
  
  // Tapa superior
  beginShape();
  for (int i = 0; i < lados; i++) {
    float angulo = map(i, 0, lados, 0, TWO_PI);
    float x = radio * cos(angulo);
    float y = radio * sin(angulo);
    vertex(x, y, altura/2);
  }
  endShape(CLOSE);
  
  // Tapa inferior
  beginShape();
  for (int i = 0; i < lados; i++) {
    float angulo = map(i, 0, lados, 0, TWO_PI);
    float x = radio * cos(angulo);
    float y = radio * sin(angulo);
    vertex(x, y, -altura/2);
  }
  endShape(CLOSE);
  
  // Lados del cilindro
  for (int i = 0; i < lados; i++) {
    float angulo1 = map(i, 0, lados, 0, TWO_PI);
    float angulo2 = map(i + 1, 0, lados, 0, TWO_PI);
    
    float x1 = radio * cos(angulo1);
    float y1 = radio * sin(angulo1);
    float x2 = radio * cos(angulo2);
    float y2 = radio * sin(angulo2);
    
    beginShape();
    vertex(x1, y1, altura/2);
    vertex(x2, y2, altura/2);
    vertex(x2, y2, -altura/2);
    vertex(x1, y1, -altura/2);
    endShape(CLOSE);
  }
  
  // Etiqueta (fuera de las transformaciones)
  popMatrix();
  pushMatrix();
  translate(120, 40, -30);
  fill(255);
  textAlign(CENTER);
  text("Escala", 0, 0, 0);
  
  popMatrix();
}

void dibujarObjetoCompuesto() {
  pushMatrix();
  
  // Transformación compuesta: Traslación circular + Rotación + Escala
  
  // 1. Traslación circular
  float radio = 80;
  float x = radio * cos(tiempo * 0.5);
  float z = radio * sin(tiempo * 0.5);
  float y = 20 * sin(tiempo);
  
  translate(x, y, z);
  
  // 2. Rotación en múltiples ejes
  rotateX(tiempo * 1.2);
  rotateY(tiempo * 0.8);
  rotateZ(tiempo * 0.6);
  
  // 3. Escala variable
  float escala = 0.8 + 0.4 * sin(tiempo * 3);
  scale(escala);
  
  // Dibujar objeto compuesto (torus aproximado con cajas)
  fill(colorCompuesto);
  stroke(0);
  strokeWeight(1);
  
  int segmentos = 8;
  float radioMayor = 30;
  float radioMenor = 8;
  
  for (int i = 0; i < segmentos; i++) {
    pushMatrix();
    
    float angulo = map(i, 0, segmentos, 0, TWO_PI);
    float xTorus = radioMayor * cos(angulo);
    float zTorus = radioMayor * sin(angulo);
    
    translate(xTorus, 0, zTorus);
    rotateY(angulo);
    
    box(radioMenor * 2, radioMenor, radioMenor);
    
    popMatrix();
  }
  
  // Etiqueta (fuera de todas las transformaciones)
  popMatrix();
  
  // Dibujar etiqueta en posición fija
  pushMatrix();
  translate(0, -150, 0);
  fill(255);
  textAlign(CENTER);
  text("Compuesta", 0, 0, 0);
  popMatrix();
}

void dibujarInformacion() {
  // Cambiar a modo 2D para el HUD
  camera();
  hint(DISABLE_DEPTH_TEST);
  
  // Fondo para el texto
  fill(0, 0, 0, 150);
  noStroke();
  rect(10, 10, 300, 120);
  
  // Información de transformaciones
  fill(255);
  textAlign(LEFT);
  textSize(12);
  
  text("Transformaciones en Tiempo Real:", 20, 30);
  text("Tiempo: " + nf(tiempo, 1, 2), 20, 50);
  text("Frame Rate: " + nf(frameRate, 1, 1) + " FPS", 20, 70);
  text("Zoom: " + nf(zoom, 1, 2), 20, 90);
  text("Ángulo X: " + nf(degrees(anguloX), 1, 1) + "°", 20, 110);
  
  // Controles
  fill(255, 255, 0);
  text("Controles: Mouse=Rotar, Rueda=Zoom, R=Reset", 20, height - 20);
  
  hint(ENABLE_DEPTH_TEST);
}

// Controles de mouse
void mouseDragged() {
  if (mouseButton == LEFT) {
    anguloY += (mouseX - pmouseX) * 0.01;
    anguloX -= (mouseY - pmouseY) * 0.01;
    
    // Limitar rotación en X
    anguloX = constrain(anguloX, -PI/2, PI/2);
  }
}

void mouseWheel(MouseEvent event) {
  float e = event.getCount();
  zoom *= (1.0 - e * 0.1);
  zoom = constrain(zoom, 0.1, 3.0);
}

// Controles de teclado
void keyPressed() {
  switch (key) {
    case 'r':
    case 'R':
      // Reiniciar animación
      tiempo = 0;
      anguloX = 0;
      anguloY = 0;
      zoom = 1.0;
      println("Animación reiniciada");
      break;
      
    case 's':
    case 'S':
      // Guardar captura
      String nombreArchivo = "transformaciones_processing_" + year() + month() + day() + "_" + hour() + minute() + second() + ".png";
      save("../resultados/" + nombreArchivo);
      println("Captura guardada: " + nombreArchivo);
      break;
      
    case ' ':
      // Pausar/reanudar animación
      if (velocidadAnimacion > 0) {
        velocidadAnimacion = 0;
        println("Animación pausada");
      } else {
        velocidadAnimacion = 0.02;
        println("Animación reanudada");
      }
      break;
  }
}
