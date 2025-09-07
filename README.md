# ArUco 
## Descripción 

Los scripts simulan un robot que debe encontrar un marcador ArUco real cuya posición exacta es desconocida, pero se tiene una posición aproximada. El robot implementa diferentes estrategias de búsqueda dependiendo de la complejidad del entorno.

## Archivos del Proyecto

### 1. `ARUCO_simple.py` - Búsqueda Básica en Espiral

**Descripción**: Implementación más simple que utiliza una búsqueda en espiral cuadrada para encontrar el marcador ArUco.

**Características**:
- **Entorno**: Espacio libre sin obstáculos
- **Estrategia**: Búsqueda en espiral cuadrada centrada en la posición aproximada

**Funcionamiento**:
1. Se genera una posición aproximada aleatoria (punto rojo)
2. Se calcula la posición real del ArUco con un offset aleatorio (punto verde)
3. El robot se mueve hacia la posición aproximada
4. Si no detecta el marcador, inicia una búsqueda en espiral cuadrada
5. La búsqueda continúa hasta encontrar el marcador o agotar el área

**Parámetros principales**:
- `PLANO = 800`: Tamaño del área de simulación
- `STEP_MOVE = 5.0`: Tamaño del paso del robot
- `RADIO = 10`: Radio de detección del marcador
- `PASOS_VUELTAS = 10`: Espaciado de la espiral
- `VUELTAS = 15`: Número máximo de vueltas en la espiral

---

### 2. `ARUCO_obstaculos.py` - Navegación con Evasión de Obstáculos

**Descripción**: Versión que añade obstáculos al entorno y implementa algoritmos básicos de evasión.

**Características**:
- **Entorno**: Espacio con obstáculos rectangulares generados aleatoriamente
- **Estrategia**: Navegación directa con evasión de obstáculos y búsqueda en espiral
- **Obstáculos**: 4 obstáculos rectangulares de tamaño variable
- **Evasión**: Búsqueda de puntos válidos cercanos cuando el objetivo está bloqueado

**Algoritmos implementados**:
1. **Detección de colisiones**: Verifica si una posición está bloqueada
2. **Verificación de camino libre**: Comprueba si hay obstáculos en la trayectoria
3. **Búsqueda de punto válido cercano**: Encuentra posiciones alternativas libres
4. **Navegación adaptativa**: Combina movimiento directo con evasión

**Funcionamiento**:
1. Genera obstáculos evitando las posiciones importantes (robot, objetivo)
2. Intenta navegación directa hacia la posición aproximada
3. Si hay obstáculos, busca rutas alternativas
4. Implementa búsqueda en espiral adaptativa evitando obstáculos

**Parámetros de obstáculos**:
- `NUM_OBSTACLES = 4`: Número de obstáculos
- `MIN_SIZE = 40`, `MAX_SIZE = 80`: Rango de tamaños de obstáculos

---

### 3. `ARUCO_A_ESTRELLA.py` - Algoritmo A* 

**Descripción**: Implementación más sofisticada que utiliza el algoritmo A* para planificación óptima de rutas en entornos con obstáculos.

**Características**:
- **Entorno**: Espacio con múltiples obstáculos complejos
- **Estrategia**: Algoritmo A* para planificación de ruta óptima + búsqueda en espiral
- **Grid**: Discretización del espacio en una malla para A*
- **Optimización**: Encuentra la ruta más corta evitando obstáculos

**Algoritmo A* implementado**:
1. **Heurística**: Distancia euclidiana al objetivo
2. **Función de costo**: Distancia recorrida + heurística
3. **Lista abierta/cerrada**: Gestión eficiente con heapq
4. **Suavizado de ruta**: Optimización de la trayectoria generada

**Componentes principales**:
- `crear_grid()`: Discretiza el espacio en celdas
- `es_celda_valida()`: Verifica si una celda está libre de obstáculos
- `a_star()`: Implementación del algoritmo A*
- `suavizar_ruta()`: Optimiza la trayectoria eliminando waypoints innecesarios
- `seguir_ruta()`: Control de movimiento del robot siguiendo la ruta

**Funcionamiento**:
1. Genera obstáculos al igual que el anterior
2. Crea un grid de navegación
3. Aplica A* para encontrar la ruta óptima hacia la posición aproximada
4. Suaviza la ruta para movimientos más naturales
5. El robot sigue la ruta planificada
6. Al llegar, ejecuta búsqueda en espiral para localizar el marcador exacto

**Parámetros A***:
- `GRID_SIZE = 5`: Resolución del grid (pixeles por celda)+


## Instalación y Uso

### Requisitos
```bash
pip install turtle
```

### Ejecución
```bash
# Versión simple
python ARUCO_simple.py

# Versión con obstáculos
python ARUCO_obstaculos.py

# Versión con A*
python ARUCO_A_ESTRELLA.py
```
