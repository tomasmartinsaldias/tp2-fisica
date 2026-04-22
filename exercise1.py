MASA = 15
GRAVEDAD = 9.81
PESO = GRAVEDAD * MASA
ROZAMIENTO = 0.1
ALTURA_OBJETIVO = 100
DELTA_T= 0.001
ENERGIA_MAX = 25000
POTENCIA_MAXIMA = 2500
F_MAX_ESTATICO = 400 #El limite que alcanza el motor, sacado del ejercicio 3

def actualizar_fuerza_rozamiento(velocidad):
    return ROZAMIENTO * velocidad**2

def fuerza_total_f(fuerza_dron, fuerza_rozamiento):
    return fuerza_dron - PESO - fuerza_rozamiento

def actualizar_posicion():
    posicion = 0
    posicion_actual = 0
    tiempo_actual = 0
    velocidad_actual = 0
    velocidad = 0
    energia = 0
        
    while posicion_actual < ALTURA_OBJETIVO:
        if velocidad != 0:
            fuerza_dron = min(F_MAX_ESTATICO, POTENCIA_MAXIMA / velocidad)
        else:
            fuerza_dron = F_MAX_ESTATICO
        
        fuerza_rozamiento = actualizar_fuerza_rozamiento(velocidad)
        aceleracion_actual = (fuerza_dron - PESO - fuerza_rozamiento)/MASA
        velocidad = velocidad_actual + aceleracion_actual*DELTA_T        
        energia += fuerza_dron * velocidad_actual * DELTA_T
        posicion = posicion_actual + velocidad*DELTA_T

        velocidad_actual = velocidad
        posicion_actual = posicion
        tiempo_actual += DELTA_T

    fuerza_total = fuerza_total_f(fuerza_dron, fuerza_rozamiento)
    print(f"Posición: {posicion}, \nVelocidad: {velocidad},\nAceleración final: {aceleracion_actual},\nTiempo: {tiempo_actual}, \nFuerza total: {fuerza_total}, \nEnergía acumulada: {energia}")
    if energia < ENERGIA_MAX:
        print("Se cumple con la restricción de energía")
    else:
        print("El plan de vuelo no cumple con la restricción de energía")

actualizar_posicion()
