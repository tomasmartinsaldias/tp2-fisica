x= 0
x_i = 0
t = 0
dt= 0.001
v_i = 0
v = 0
MASA = 15
ACELERACION_INICIAL = 5
GRAVEDAD = 9.81
PESO = GRAVEDAD * MASA
ROZAMIENTO = 0.1
pot_max = 2500
work_max = 25000

y_obj = 100
y_i = 0

trabajo_acum = 0
potencia_acum = 0


while x_i < y_obj:
    fuerza_dron = ACELERACION_INICIAL * MASA
    if v != 0:
        fuerza_dron = min(fuerza_dron, pot_max / v)
    
    fuerza_rozamiento = ROZAMIENTO * v**2    
    fuerza_total = fuerza_dron + fuerza_rozamiento + PESO
    a_i = fuerza_dron / MASA
    v = v_i + a_i*dt
    x= x_i + v*dt
    
    trabajo = fuerza_dron * (x - x_i)
    trabajo_acum += trabajo
    
    potencia= fuerza_dron *(v-v_i) 
    potencia_acum += potencia
    
    
    v_i = v
    x_i = x
    t += dt


print(f"x: {x}, v: {v}, a_i: {a_i}, t: {t}, fuerza_dron: {fuerza_dron}, fuerza_rozamiento: {fuerza_rozamiento}, fuerza_total: {fuerza_total}, trabajo_acum: {trabajo_acum}, potencia_acum: {potencia_acum}")
