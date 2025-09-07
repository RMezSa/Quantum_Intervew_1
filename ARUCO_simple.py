import turtle, random, math, time

PLANO = 800
STEP_MOVE = 5.0
SLEEP = 0.01
PASOS_VUELTAS = 10     
VUELTAS = 15     
RADIO = 10     

wn = turtle.Screen()
wn.title("ArUco")
wn.bgcolor("white")
wn.setup(width=PLANO, height=PLANO)

bot = turtle.Turtle(); bot.shape("square"); bot.color("black"); bot.penup(); bot.speed(0)
APROXIMADA = turtle.Turtle(); APROXIMADA.hideturtle(); APROXIMADA.penup()
REAL = turtle.Turtle();  REAL.hideturtle();  REAL.penup()

def dibujar(t, x, y, color="black", size=8):
    t.goto(x, y); t.dot(size, color)

def distancia_puntos(a, b, c, d):
    return math.hypot(a - c, b - d)

def moverse(x, y, check_detect):
    while True:
        dx, dy = x - bot.xcor(), y - bot.ycor()
        d = math.hypot(dx, dy)
        if d < 0.5:
            return check_detect()  

        angle = math.degrees(math.atan2(dy, dx))
        bot.setheading(angle)
        bot.pendown()
        bot.forward(min(STEP_MOVE, d))
        found = check_detect()
        print(f"Robot ({bot.xcor():.2f}, {bot.ycor():.2f}) => Objetivo ({x:.2f}, {y:.2f})  | Found={found}")
        if found:
            return True
        time.sleep(SLEEP)

def spiral_square_waypoints(cx, cy, step, turns):
    x, y = cx, cy
    for i in range(1, turns + 1):
        yield (cx + step * i, cy)               # derecha
        yield (cx + step * i, cy + step * i)    # arriba
        yield (cx - step * i, cy + step * i)    # izquierda
        yield (cx - step * i, cy - step * i)    # abajo
        yield (cx + step * (i + 1), cy - step * i)  # afuera y derecha

x_aprox = random.randint(-PLANO//2 + 200, PLANO//2 - 200)
y_aprox = random.randint(-PLANO//2 + 250, PLANO//2 - 250)

offset_r = random.randint(10, 50)
offset_th = random.uniform(0, 2*math.pi)
x_real = x_aprox + offset_r * math.cos(offset_th)
y_real = y_aprox + offset_r * math.sin(offset_th)

dibujar(APROXIMADA, x_aprox, y_aprox, "red", 10)     # POSICION APROXIMADA
dibujar(REAL,  x_real,  y_real,  "green", 8)    # posición real 

print(f"Aprox     : ({x_aprox:.2f}, {y_aprox:.2f})")
print(f"ArUco real: ({x_real:.2f}, {y_real:.2f})")
print(f"RADIO     : {RADIO} px")

bot.goto(0, 0)

def detected():
    return distancia_puntos(bot.xcor(), bot.ycor(), x_real, y_real) <= RADIO

found = moverse(x_aprox, y_aprox, detected)
if found:
    print("Posicion encontrada.")
    turtle.done(); quit()

for (wx, wy) in spiral_square_waypoints(x_aprox, y_aprox, PASOS_VUELTAS, VUELTAS):
    found = moverse(wx, wy, detected)
    if found:
        print("Detección.")
        break

if not found:
    print("No hubo detección dentro del área explorada.")

turtle.done()