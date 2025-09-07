import turtle, random, math, time
import heapq

PLANO = 800
STEP_MOVE = 5.0
SLEEP = 0.01
PASOS_VUELTAS = 10     
VUELTAS = 15     
RADIO = 12     

# Obstáculos
NUMERO_OBS = 3
SIZE_MIN = 60
SIZE_MAXIMO = 150
MARGEN_OBSTACULO = 80  

# A* 
GRID_SIZE = 5
RADIO_TORTUGA = 12 

wn = turtle.Screen()
wn.title("ArUco con A* y Obstáculos")
wn.bgcolor("white")
wn.setup(width=PLANO, height=PLANO)

bot = turtle.Turtle(); 
bot.shape("turtle");
bot.color("black");
bot.penup(); 
bot.speed(0)

APROXIMADA = turtle.Turtle(); APROXIMADA.hideturtle(); APROXIMADA.penup()
REAL = turtle.Turtle();  REAL.hideturtle();  REAL.penup()
DIBUJADOR_OBSTACULO = turtle.Turtle(); DIBUJADOR_OBSTACULO.hideturtle(); DIBUJADOR_OBSTACULO.penup(); DIBUJADOR_OBSTACULO.speed(0)

obstaculos_lista = []

def dibujar_punto(t, x, y, color="black", size=8):
    t.goto(x, y); t.dot(size, color)

def distancia_puntos(a, b, c, d):
    return math.hypot(a - c, b - d)

def generar_obstaculos(robot_start, approx_pos, real_pos):
    global obstaculos_lista
    obstaculos_lista = []
    
    areas_antiobstaculos = [
        (robot_start[0], robot_start[1], 30, 30), 
        (approx_pos[0], approx_pos[1], 40, 40),   
        (real_pos[0], real_pos[1], 40, 40)        
    ]
    
    for _ in range(NUMERO_OBS):
        attempts = 0
        while attempts < 100: 
            x = random.randint(-PLANO//2 + MARGEN_OBSTACULO, PLANO//2 - MARGEN_OBSTACULO)
            y = random.randint(-PLANO//2 + MARGEN_OBSTACULO, PLANO//2 - MARGEN_OBSTACULO)
            # Tamaño
            width = random.randint(SIZE_MIN, SIZE_MAXIMO)
            height = random.randint(SIZE_MIN, SIZE_MAXIMO)
            #Overlapping
            nuevo = (x, y, width, height)
            if not overlaps_with_existing(nuevo) and not overlaps_con_areas(nuevo, areas_antiobstaculos):
                obstaculos_lista.append(nuevo)
                break
            attempts += 1
    
    print(f"{len(obstaculos_lista)} obstáculos generados")

def overlaps_con_areas(nuevo, areas_antiobstaculos):
    x1, y1, w1, h1 = nuevo

    for px, py, pw, ph in areas_antiobstaculos:
        margin = 25
        area_x = px - pw//2
        area_y = py - ph//2
        
        if (x1 < area_x + pw + margin and x1 + w1 + margin > area_x and
            y1 < area_y + ph + margin and y1 + h1 + margin > area_y):
            return True
    return False

def overlaps_with_existing(nuevo):
    x1, y1, w1, h1 = nuevo

    for x2, y2, w2, h2 in obstaculos_lista:
        #Margen entre obstaculos
        margin = 20
        if (x1 < x2 + w2 + margin and x1 + w1 + margin > x2 and
            y1 < y2 + h2 + margin and y1 + h1 + margin > y2):
            return True
    return False

def dibujar_obstaculos():
    DIBUJADOR_OBSTACULO.color("gray")
    for x, y, width, height in obstaculos_lista:
        dibujar_rectangulo(x, y, width, height)

def dibujar_rectangulo(x, y, width, height):
    DIBUJADOR_OBSTACULO.goto(x, y)
    DIBUJADOR_OBSTACULO.pendown()
    DIBUJADOR_OBSTACULO.begin_fill()
    
    for _ in range(2):
        DIBUJADOR_OBSTACULO.forward(width)
        DIBUJADOR_OBSTACULO.left(90)
        DIBUJADOR_OBSTACULO.forward(height)
        DIBUJADOR_OBSTACULO.left(90)
    
    DIBUJADOR_OBSTACULO.end_fill()
    DIBUJADOR_OBSTACULO.penup()

def punto_en_obstaculo(px, py):
    for x, y, width, height in obstaculos_lista:
        if x <= px <= x + width and y <= py <= y + height:
            return True
    return False

def validar_posiciones(px, py):
    for x, y, width, height in obstaculos_lista:
        if (x - RADIO_TORTUGA <= px <= x + width + RADIO_TORTUGA and 
            y - RADIO_TORTUGA <= py <= y + height + RADIO_TORTUGA):
            return False
    
    boundary = PLANO // 2 - RADIO_TORTUGA
    if not (-boundary <= px <= boundary and -boundary <= py <= boundary):
        return False
        
    return True

def world_to_grid(wx, wy):
    gx = int((wx + PLANO // 2) // GRID_SIZE)
    gy = int((wy + PLANO // 2) // GRID_SIZE)
    return gx, gy

def grid_to_world(gx, gy):
    wx = gx * GRID_SIZE - PLANO // 2 + GRID_SIZE // 2
    wy = gy * GRID_SIZE - PLANO // 2 + GRID_SIZE // 2
    return wx, wy

def heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_nodos_vecinos(node):
    x, y = node
    vecinos = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            max_grid = PLANO // GRID_SIZE
            if 0 <= nx < max_grid and 0 <= ny < max_grid:
                wx, wy = grid_to_world(nx, ny)
                if validar_posiciones(wx, wy):
                    cost = math.sqrt(2) if abs(dx) + abs(dy) == 2 else 1
                    vecinos.append(((nx, ny), cost))
    return vecinos

def astar_path(start_world, goal_world):
    start = world_to_grid(*start_world)
    goal = world_to_grid(*goal_world)
    
    if not validar_posiciones(*start_world) or not validar_posiciones(*goal_world):
        print(f"[ERROR] Invalid start {start_world} or goal {goal_world}")
        return []
    
    open_set = [(0.0, 0, start)] 
    closed_set = set()  
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    counter = 0
    
    while open_set:
        current = heapq.heappop(open_set)[2]
        
        if current in closed_set:
            continue
            
        closed_set.add(current)
        
        if current == goal:
            grid_path = []
            while current in came_from:
                grid_path.append(current)
                current = came_from[current]
            grid_path.append(start)
            grid_path.reverse()
            
            world_path = [grid_to_world(*node) for node in grid_path]
            smoothed_path = smooth_path(world_path, start_world, goal_world)
            return smoothed_path
        
        for neighbor, move_cost in get_nodos_vecinos(current):
            if neighbor in closed_set:
                continue
                
            tentative_g = g_score[current] + move_cost
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                counter += 1
                heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
    
    print(f"Sin camino")
    return []  

def smooth_path(path, start_world, goal_world):
    if len(path) <= 2:
        return [start_world, goal_world]
    
    smoothed = [start_world]
    current_idx = 0
    
    while current_idx < len(path) - 1:
        farthest_idx = current_idx + 1
        
        for i in range(current_idx + 2, len(path)):
            if has_line_of_sight(path[current_idx], path[i]):
                farthest_idx = i
            else:
                break
        
        if farthest_idx < len(path) - 1:
            smoothed.append(path[farthest_idx])
        
        current_idx = farthest_idx
    
    smoothed.append(goal_world)
    
    final_path = [smoothed[0]]
    for i in range(1, len(smoothed)):
        if smoothed[i] != final_path[-1]:
            final_path.append(smoothed[i])
    
    return final_path

def has_line_of_sight(start, end):
    x1, y1 = start
    x2, y2 = end
    
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    if distance == 0:
        return True
        
    steps = max(int(distance / (GRID_SIZE / 2)), 1)
    
    for i in range(steps + 1):
        t = i / steps
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        
        if not validar_posiciones(x, y):
            return False
    
    return True

def moverse(x, y, check_detect):
    target_pos = (x, y)

    while True:
        cx, cy = bot.xcor(), bot.ycor()
        dx, dy = x - cx, y - cy
        d = math.hypot(dx, dy)

        if d < 0.5:
            return check_detect()
        if has_line_of_sight((cx, cy), target_pos):
            angle = math.degrees(math.atan2(dy, dx))
            bot.setheading(angle)
            bot.pendown()
            bot.forward(min(STEP_MOVE, d))

            found = check_detect()
            if found:
                print("[OK] Target detected during movement!")
                return True
            time.sleep(SLEEP)
            continue

        path = astar_path((cx, cy), target_pos)
        if not path or len(path) < 2:
            return check_detect()

        for (wx, wy) in path[1:]:
            while True:
                cx, cy = bot.xcor(), bot.ycor()
                if has_line_of_sight((cx, cy), target_pos):
                    break

                dx, dy = wx - cx, wy - cy
                d = math.hypot(dx, dy)
                if d < 0.5:
                    break

                angle = math.degrees(math.atan2(dy, dx))
                bot.setheading(angle)
                bot.pendown()
                bot.forward(min(STEP_MOVE, d))

                found = check_detect()
                if found:
                    print("[OK] Target detected during movement!")
                    return True
                time.sleep(SLEEP)

def spiral_square_waypoints(cx, cy, step, turns):
    x, y = cx, cy
    for i in range(1, turns + 1):
        candidates = [
            (cx + step * i, cy),               # derecha
            (cx + step * i, cy + step * i),    # arriba
            (cx - step * i, cy + step * i),    # izquierda
            (cx - step * i, cy - step * i),    # abajo
            (cx + step * (i + 1), cy - step * i)  # siguiente brazo derecha
        ]
        
        for wx, wy in candidates:
            if validar_posiciones(wx, wy):
                yield (wx, wy)
            

x_aprox = random.randint(-PLANO//2 + 100, PLANO//2 - 100)
y_aprox = random.randint(-PLANO//2 + 100, PLANO//2 - 100)

offset_r = random.randint(25, 50)
offset_th = random.uniform(0, 2*math.pi)
x_real = x_aprox + offset_r * math.cos(offset_th)
y_real = y_aprox + offset_r * math.sin(offset_th)

generar_obstaculos((0, 0), (x_aprox, y_aprox), (x_real, y_real))
dibujar_obstaculos()

dibujar_punto(APROXIMADA, x_aprox, y_aprox, "red", 10)
dibujar_punto(REAL,  x_real,  y_real,  "green", 8)    # posición real 

print(f"Aprox     : ({x_aprox:.2f}, {y_aprox:.2f})")
print(f"ArUco real: ({x_real:.2f}, {y_real:.2f})")
print(f"RADIO     : {RADIO} px")

bot.goto(0, 0)

def detected():
    return distancia_puntos(bot.xcor(), bot.ycor(), x_real, y_real) <= RADIO

found = moverse(x_aprox, y_aprox, detected)
if found:
    print("DETECCION")
    turtle.done(); quit()

for (wx, wy) in spiral_square_waypoints(x_aprox, y_aprox, PASOS_VUELTAS, VUELTAS):
    found = moverse(wx, wy, detected)
    if found:
        print("[OK] ArUco DETECTADO.")
        break
turtle.done()
