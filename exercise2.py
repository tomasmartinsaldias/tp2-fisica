import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ORIGEN = np.array([0,0,0])
DESTINO = np.array([80,50,60])
V_VIENTO = np.array([5,-2,0]) #m/s
K_ARRASTRE = 0.15 #kg/s
POTENCIA_MAXIMA = 3000 #W\
MASA = 15 #kg
GRAVEDAD = -9.81 #m/s**2
PESO = np.array([0,0,MASA*GRAVEDAD])
POTENCIA_MAXIMA = 3000 # P = Fuerza * Velocidad
DELTA_T = 0.001
F_MAX_ESTATICO = 400 #El limite que alcanza el motor, sacado del ejercicio 3
UMBRAL_LLEGADA = 1

def actualizar_fuerza_rozamiento(v_dron):
    v_rel = v_dron - V_VIENTO
    norma_v_rel = np.linalg.norm(v_rel)
    return -K_ARRASTRE * norma_v_rel * v_rel #Esto es la simplificación de -k*v**2*|v|

def trayectoria():
    # Creamos variables de historial para graficar después
    h_pos, h_tiempo, h_vel = [], [], []
    h_pot_x, h_pot_y = [], []
    h_f_motor, h_f_fric = [], []

    posicion = ORIGEN
    v_dron = np.array([0,0,0])
    aceleracion = np.array([0,0,0])
    energia = 0
    tiempo_actual = 0
    distancia_al_objetivo = np.linalg.norm(DESTINO - posicion)

    while distancia_al_objetivo > UMBRAL_LLEGADA:
        # Trayectoria del Dron
        vector_trayectoria = DESTINO - posicion
        # Dirección de la fuerza del dron
        versor_u = vector_trayectoria / np.linalg.norm(vector_trayectoria)
        f_viento = actualizar_fuerza_rozamiento(v_dron)

        # Primero calculamos la velocidad proyectada en la dirección del movimiento
        velocidad_proyectada = v_dron @ versor_u

        if velocidad_proyectada > 0.01: # Un pequeño umbral para evitar divisiones por cero
            limite_potencia = POTENCIA_MAXIMA / velocidad_proyectada
            f_dron_magn = min(F_MAX_ESTATICO, limite_potencia)
        else:
            f_dron_magn = F_MAX_ESTATICO

        f_dron_vector = f_dron_magn*versor_u
        
        aceleracion = (f_dron_vector + PESO + f_viento)/MASA
        v_dron = v_dron + aceleracion*DELTA_T
        energia += f_dron_magn * (v_dron@versor_u) * DELTA_T
        posicion = posicion + v_dron*DELTA_T
        tiempo_actual += DELTA_T

        distancia_al_objetivo = np.linalg.norm(DESTINO - posicion)

        # --- Guardamos los datos de cada iteración ---
        h_pos.append(posicion.copy())
        h_tiempo.append(tiempo_actual)
        h_vel.append(v_dron.copy())
        h_pot_x.append(f_dron_vector[0] * v_dron[0])
        h_pot_y.append(f_dron_vector[1] * v_dron[1])
        h_f_motor.append(f_dron_magn)
        h_f_fric.append(np.linalg.norm(f_viento))

    # Convertimos a arrays de numpy para graficar fácil
    h_pos = np.array(h_pos)
    h_vel = np.array(h_vel)

    # --- Generación de Gráficos ---
    
    # 1. Trayectoria 3D
    fig1 = plt.figure(figsize=(8, 6))
    ax = fig1.add_subplot(111, projection='3d')
    ax.plot(h_pos[:,0], h_pos[:,1], h_pos[:,2], label='Vuelo real')
    ax.scatter(*DESTINO, color='red', label='Destino B')
    ax.set_title("Trayectoria 3D del Dron")
    ax.set_xlabel("X (m)"); ax.set_ylabel("Y (m)"); ax.set_zlabel("Z (m)")

    # 2. Potencias X e Y vs Tiempo
    plt.figure(figsize=(10, 4))
    plt.plot(h_tiempo, h_pot_x, label='Potencia en X', color='orange')
    plt.plot(h_tiempo, h_pot_y, label='Potencia en Y', color='purple')
    plt.title("Evolución de Potencia por Eje")
    plt.xlabel("Tiempo (s)"); plt.ylabel("Potencia (W)")
    plt.legend(); plt.grid(True)

    # 3. Velocidades por componente
    plt.figure(figsize=(10, 4))
    plt.plot(h_tiempo, h_vel[:,0], label='Vx', color='r')
    plt.plot(h_tiempo, h_vel[:,1], label='Vy', color='g')
    plt.plot(h_tiempo, h_vel[:,2], label='Vz', color='b')
    plt.title("Velocidad en el tiempo")
    plt.xlabel("Tiempo (s)"); plt.ylabel("m/s")
    plt.legend(); plt.grid(True)

    # 4. Magnitud de Fuerzas
    plt.figure(figsize=(10, 4))
    plt.plot(h_tiempo, h_f_motor, label='Fuerza Motor (Empuje)', color='black')
    plt.plot(h_tiempo, h_f_fric, label='Fuerza Fricción (Arrastre)', color='gray', linestyle='--')
    plt.axhline(y=F_MAX_ESTATICO, color='red', linestyle=':', label='Límite Estático')
    plt.title("Fuerza del Motor vs. Fuerza de Fricción")
    plt.xlabel("Tiempo (s)"); plt.ylabel("Fuerza (N)")
    plt.legend(); plt.grid(True)

    plt.show()

trayectoria()





