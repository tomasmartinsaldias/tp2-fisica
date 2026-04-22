import numpy as np

ORIGEN = np.array([0,0,0])
DESTINO = np.array([80,50,60])
V_VIENTO = np.array([5,-2,0]) #m/s
K_ARRASTRE = 0.15 #kg/s
POTENCIA_MAXIMA = 3000 #W


def actualizar_fuerza_rozamiento(v_dron):
    v_rel = v_dron - V_VIENTO
    norma_v_rel = np.linalg.norm(v_rel)
    versor_u = vector_trayectoria / np.linalg.norm(vector_trayectoria)
    return -K_ARRASTRE*norma_v_rel*v_rel


