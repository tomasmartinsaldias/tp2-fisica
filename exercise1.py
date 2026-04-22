MASA = 15
GRAVEDAD = 9.81
PESO = GRAVEDAD * MASA
ROZAMIENTO = 0.1
ALTURA_OBJETIVO = 100
ACELERACION_INICIAL = (PESO + 1)/MASA
DELTA_T= 0.001
ENERGIA_MAX = 25000
POTENCIA_MAXIMA = 2500

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
    fuerza_dron = ACELERACION_INICIAL * MASA
        
    while posicion_actual < ALTURA_OBJETIVO:
        if velocidad != 0:
            fuerza_dron = min(fuerza_dron, POTENCIA_MAXIMA / velocidad)
        
        fuerza_rozamiento = actualizar_fuerza_rozamiento(velocidad)
        aceleracion_actual = (fuerza_dron - PESO - fuerza_rozamiento)/MASA
        velocidad = velocidad_actual + aceleracion_actual*DELTA_T        
        energia += fuerza_dron * velocidad_actual * DELTA_T
        posicion = posicion_actual + velocidad*DELTA_T

        velocidad_actual = velocidad
        posicion_actual = posicion
        tiempo_actual += DELTA_T

    fuerza_total = fuerza_total_f(fuerza_dron, fuerza_rozamiento)
    print(ACELERACION_INICIAL)
    print(f"Posición: {posicion}, \nVelocidad: {velocidad},\nAceleración final: {aceleracion_actual},\nTiempo: {tiempo_actual}, \nFuerza total: {fuerza_total}, \nFuerza rozamiento: {fuerza_rozamiento}")

actualizar_posicion()