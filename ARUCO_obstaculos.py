
import turtle
import random
import math
import time

# Configuración básica
WINDOW_SIZE = 500
STEP_SIZE = 5
RADIO = 10
PASOS_VUELTAS = 15
VUELTAS = 8

# Obstáculos
NUM_OBSTACLES = 4
MIN_SIZE = 40
MAX_SIZE = 80

# Setup
screen = turtle.Screen()
screen.title("Busqueda con obstaculos")
screen.bgcolor("white")
screen.setup(width=WINDOW_SIZE, height=WINDOW_SIZE)

# Robot
robot = turtle.Turtle()
robot.shape("turtle")
robot.color("black")
robot.penup()
robot.speed(0)

REAL = turtle.Turtle()
REAL.hideturtle()
REAL.penup()

APPROXIMADA = turtle.Turtle()
APPROXIMADA.hideturtle()
APPROXIMADA.penup()

dibujador_obstaculos = turtle.Turtle()
dibujador_obstaculos.hideturtle()
dibujador_obstaculos.penup()
dibujador_obstaculos.speed(0)

obstaculos = []

def dibujar_punto(turtle_obj, x, y, color="red", size=10):
    turtle_obj.goto(x, y)
    turtle_obj.dot(size, color)

def distancia(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def generar_obstaculos(robot_start, approx_pos, real_pos):
    global obstaculos
    obstaculos = []
    
    # Áreas a evitar
    protected_areas = [robot_start, approx_pos, real_pos]
    
    for _ in range(NUM_OBSTACLES):
        attempts = 0
        while attempts < 50:
            x = random.randint(-WINDOW_SIZE//2 + 60, WINDOW_SIZE//2 - 60)
            y = random.randint(-WINDOW_SIZE//2 + 60, WINDOW_SIZE//2 - 60)
            width = random.randint(MIN_SIZE, MAX_SIZE)
            height = random.randint(MIN_SIZE, MAX_SIZE)
            
            cerca = False
            for px, py in protected_areas:
                if distancia(x + width/2, y + height/2, px, py) < 80:
                    cerca = True
                    break
            
            if not cerca:
                obstaculos.append((x, y, width, height))
                break
            attempts += 1

def dibujar_obstaculos():
    dibujador_obstaculos.color("gray")
    for x, y, width, height in obstaculos:
        dibujar_rectangulo(x, y, width, height)

def dibujar_rectangulo(x, y, width, height):
    dibujador_obstaculos.goto(x, y)
    dibujador_obstaculos.pendown()
    dibujador_obstaculos.begin_fill()
    
    for _ in range(2):
        dibujador_obstaculos.forward(width)
        dibujador_obstaculos.left(90)
        dibujador_obstaculos.forward(height)
        dibujador_obstaculos.left(90)
    
    dibujador_obstaculos.end_fill()
    dibujador_obstaculos.penup()

def posicion_bloqueada(x, y, margin=8):
    for ox, oy, width, height in obstaculos:
        if (ox - margin <= x <= ox + width + margin and 
            oy - margin <= y <= oy + height + margin):
            return True
    return False

def camino_libre(x1, y1, x2, y2):
    dist = distancia(x1, y1, x2, y2)
    if dist == 0:
        return True
    
    steps = int(dist / 5) + 1
    for i in range(steps + 1):
        t = i / steps if steps > 0 else 0
        check_x = x1 + t * (x2 - x1)
        check_y = y1 + t * (y2 - y1)
        
        if posicion_bloqueada(check_x, check_y, 8):
            return False
    return True

def find_nearest_valid_point(target_x, target_y, max_distance=100):
    
    for distance in range(10, max_distance, 8):
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            test_x = target_x + distance * math.cos(rad)
            test_y = target_y + distance * math.sin(rad)
            
            # Verificar límites
            if abs(test_x) > WINDOW_SIZE//2 - 20 or abs(test_y) > WINDOW_SIZE//2 - 20:
                continue
                
            if not posicion_bloqueada(test_x, test_y):
                current_x, current_y = robot.xcor(), robot.ycor()
                if camino_libre(current_x, current_y, test_x, test_y):
                    return test_x, test_y
    return None

def navegar(target_x, target_y):
    current_x, current_y = robot.xcor(), robot.ycor()
    
    if posicion_bloqueada(target_x, target_y):
        cercano = find_nearest_valid_point(target_x, target_y)
        if cercano:
            target_x, target_y = cercano
        else:
            return False
    
    # Intentar ir directamente
    if camino_libre(current_x, current_y, target_x, target_y):
        return move_straight_to(target_x, target_y)
    
    # Rodear
    detour_offsets = [
        # Rodeos pequeños
        (40, 0), (-40, 0), (0, 40), (0, -40),
        (40, 40), (-40, 40), (40, -40), (-40, -40),
        # Rodeos grandes
        (80, 0), (-80, 0), (0, 80), (0, -80),
        (80, 80), (-80, 80), (80, -80), (-80, -80),
        # Rodeos medios
        (60, 30), (-60, 30), (60, -30), (-60, -30),
        (30, 60), (-30, 60), (30, -60), (-30, -60)
    ]
    
    for dx, dy in detour_offsets:
        via_x = current_x + dx
        via_y = current_y + dy
        
        # Verificar límites
        if abs(via_x) > WINDOW_SIZE//2 - 30 or abs(via_y) > WINDOW_SIZE//2 - 30:
            continue
            
        if (not posicion_bloqueada(via_x, via_y) and
            camino_libre(current_x, current_y, via_x, via_y) and 
            camino_libre(via_x, via_y, target_x, target_y)):
            
            found = move_straight_to(via_x, via_y)
            if found:
                return True
            
            return move_straight_to(target_x, target_y)
    
    escape_point = find_nearest_valid_point(current_x, current_y, 60)
    if escape_point:
        print(f"Escapando a ({escape_point[0]}, {escape_point[1]})")
        move_straight_to(escape_point[0], escape_point[1])
    else:
        print(f"({target_x:.1f}, {target_y:.1f}) - completamente bloqueado")
    
    return False

def move_straight_to(target_x, target_y):
    current_x, current_y = robot.xcor(), robot.ycor()
    
    dx = target_x - current_x
    dy = target_y - current_y
    dist = math.sqrt(dx**2 + dy**2)
    
    if dist < 2:
        return is_target_detected()
    
    angle = math.degrees(math.atan2(dy, dx))
    robot.setheading(angle)
    robot.pendown()
    
    steps = int(dist / STEP_SIZE) + 1
    step_x = dx / steps
    step_y = dy / steps
    
    for i in range(steps):
        new_x = current_x + step_x * (i + 1)
        new_y = current_y + step_y * (i + 1)
        robot.goto(new_x, new_y)
        print(f"Robot ({robot.xcor():.2f}, {robot.ycor():.2f}) => Objetivo ({real_x:.2f}, {real_y:.2f})")
        time.sleep(0.03)
        
        if is_target_detected():
            return True
    
    robot.penup()
    return False

def is_target_detected():
    robot_x, robot_y = robot.xcor(), robot.ycor()
    return distancia(robot_x, robot_y, real_x, real_y) <= RADIO

def spiral_square_waypoints(cx, cy, step, turns):
    for i in range(1, turns + 1):
        yield (cx + step * i, cy)               # derecha
        yield (cx + step * i, cy + step * i)    # arriba
        yield (cx - step * i, cy + step * i)    # izquierda
        yield (cx - step * i, cy - step * i)    # abajo
        yield (cx + step * (i + 1), cy - step * i)  # afuera y derecha

def spiral_search(center_x, center_y):
    
    for (wx, wy) in spiral_square_waypoints(center_x, center_y, PASOS_VUELTAS, VUELTAS):
        if abs(wx) > WINDOW_SIZE//2 - 40 or abs(wy) > WINDOW_SIZE//2 - 40:
            print(f"({wx}, {wy}) - fuera de límites")
            continue
        
        if posicion_bloqueada(wx, wy):
            print(f"({wx}, {wy}) - bloqueado")
            continue
        
        print(f"Navegacion: ({wx}, {wy})")
        found = navegar(wx, wy)
        
        if found or is_target_detected():
            print("DETECCION")
            return True
    
    return False

approx_x = random.randint(-WINDOW_SIZE//2 + 120, WINDOW_SIZE//2 - 120)
approx_y = random.randint(-WINDOW_SIZE//2 + 120, WINDOW_SIZE//2 - 120)

offset_distance = random.randint(25, 60)
offset_angle = random.uniform(0, 2 * math.pi)
real_x = approx_x + offset_distance * math.cos(offset_angle)
real_y = approx_y + offset_distance * math.sin(offset_angle)

generar_obstaculos((0, 0), (approx_x, approx_y), (real_x, real_y))
dibujar_obstaculos()

# Dibujar marcadores
dibujar_punto(APPROXIMADA, approx_x, approx_y, "orange", 12)
dibujar_punto(REAL, real_x, real_y, "red", 8)

print(f"Posicion aproximada: ({approx_x:.1f}, {approx_y:.1f})")
print(f"Posicion real del objetivo: ({real_x:.1f}, {real_y:.1f})")
print(f"Radio de deteccion: {RADIO}")
print(f"Obstaculos generados: {len(obstaculos)}")

robot.goto(0, 0)

print("\nFase 1")
found = navegar(approx_x, approx_y)

if found:
    print("DETECCION")
else:
    current_x, current_y = robot.xcor(), robot.ycor()
    spiral_center = find_nearest_valid_point(approx_x, approx_y, 150)
    
    if spiral_center and (spiral_center[0] != approx_x or spiral_center[1] != approx_y):
        navegar(spiral_center[0], spiral_center[1])
        approx_x, approx_y = spiral_center
    else:
        approx_x, approx_y = current_x, current_y 
    
    # Fase 2: Búsqueda en espiral
    print("\nFase 2")
    found = spiral_search(approx_x, approx_y)
    
    if found:
        print("DETECCION")
    else:
        print("NO HUBO DETECCION")

screen.exitonclick()
