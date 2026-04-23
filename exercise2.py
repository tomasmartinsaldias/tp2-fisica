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

    trabajo_aire = 0

    while distancia_al_objetivo > UMBRAL_LLEGADA and (tiempo_actual < 20) and (energia < 40000):
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
        
        # f = m*a --> a = f/m
        aceleracion = (f_dron_vector + PESO + f_viento)/MASA
        # actualizamos velocidad
        v_dron = v_dron + aceleracion*DELTA_T
        # actualizamos la energía acumuladq (como es una magnitud transformo el vector en magnitud haciendo el producto escalar con el versor direccion)
        energia += f_dron_magn * (v_dron@versor_u) * DELTA_T
        posicion = posicion + v_dron*DELTA_T
        tiempo_actual += DELTA_T

        distancia_al_objetivo = np.linalg.norm(DESTINO - posicion)

        trabajo_aire += (f_viento @ v_dron) * DELTA_T

        # --- Guardamos los datos de cada iteración ---
        h_pos.append(posicion.copy())
        h_tiempo.append(tiempo_actual)
        h_vel.append(v_dron.copy())
        h_pot_x.append(f_dron_vector[0] * v_dron[0])
        h_pot_y.append(f_dron_vector[1] * v_dron[1])
        h_f_motor.append(f_dron_magn)
        h_f_fric.append(np.linalg.norm(f_viento))

    # Datos oara el balance energético
    u_final = MASA * abs(GRAVEDAD) * (posicion[2] - ORIGEN[2])
    k_final = 0.5 * MASA * np.linalg.norm(v_dron)**2 #Energía cinética
    cambio_energia_mecanica = k_final + u_final
    suma_trabajos = energia + trabajo_aire
    error_trabajo_energia = abs(suma_trabajos - cambio_energia_mecanica)

    print(f"Suma de Trabajo Dron + Aire: {suma_trabajos:.2f} J")
    print(f"Cambio en la Energía Mecánica: {cambio_energia_mecanica:.2f} J")
    print(f"Error numérico absoluto: {error_trabajo_energia:.4f} J")
    print(f"Porcentaje que representa el error: {(error_trabajo_energia/((suma_trabajos+cambio_energia_mecanica)/2)*100):.3f}%")

    print("--- RESULTADO DE LA MISIÓN ---")
    if distancia_al_objetivo <= UMBRAL_LLEGADA:
        print(f"✅ ¡ÉXITO! Destino alcanzado en {tiempo_actual:.2f} s")
    elif tiempo_actual >= 20:
        print(f"❌ FALLO: Tiempo límite excedido (Misión abortada a los 20 s)")
    elif energia >= 40000:
        print(f"❌ FALLO: Batería agotada (Consumo superó los 40,000 J)")

    print(f"Distancia final al objetivo: {distancia_al_objetivo:.2f} m")
    print(f"Energía total consumida: {energia:.2f} J")

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

    # 3. Fuerza del Motor vs Fricción
    plt.figure(figsize=(10, 4))
    plt.plot(h_tiempo, h_f_motor, label='Fuerza Motor (Empuje)', color='black', linewidth=2)
    plt.plot(h_tiempo, h_f_fric, label='Fuerza Fricción (Arrastre)', color='gray', linestyle='--')
    
    # Agregamos la línea horizontal roja que marca tu límite físico
    plt.axhline(y=F_MAX_ESTATICO, color='red', linestyle=':', label='Límite Estático (400 N)')
    
    plt.title("Fuerza del Motor vs. Fuerza de Fricción")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Fuerza (N)")
    plt.legend()
    plt.grid(True)
    
    plt.show()

trayectoria()





