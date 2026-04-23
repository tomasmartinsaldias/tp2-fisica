import numpy as np

# Constantes
MASA  = 15
GRAVEDAD = 9.81
PESO = GRAVEDAD * MASA
ROZAMIENTO = 0.15
POTENCIA_MAX= 3000
POSICION_INICIAL = np.array([0.0, 0.0, 0.0])
POSICION_FINAL = np.array([80.0, 50.0, 60.0])
VIENTO = np.array([5.0, -2.0, 0.0])
DELTA_T = 0.01
F_MAX_ESTATICO = 400

def get_vectors_unitarios(pos_inicial, pos_final):
    vector = np.array(pos_final) - np.array(pos_inicial)
    distancia = np.linalg.norm(vector)
    if distancia == 0:
        return np.zeros_like(vector), 0
    return vector / distancia, distancia

def decompose_wind(vel_viento, vector_unitario):
    viento_vector = vel_viento
    projection_scalar = np.dot(viento_vector, vector_unitario)
    projection_vector = projection_scalar * vector_unitario
    ortogonal_wind = viento_vector - projection_vector
    return projection_scalar, ortogonal_wind

def actualizar_fuerza_rozamiento(velocidad_relativa):
    return ROZAMIENTO * velocidad_relativa**2

def get_max_speed(potencia_max, velocidad_viento, indice_rozamiento):
    v_max = (potencia_max / indice_rozamiento)**(1/3)
    return v_max

def navegator(ortogonal_wind, vector_unitario, v_max):
    norma_ortogonal = np.linalg.norm(ortogonal_wind)
    if norma_ortogonal > v_max:
        return None # Caso error
    obj_speed = np.sqrt(v_max**2 - norma_ortogonal**2)
    # El vector del dron compensa el viento ortogonal
    return (vector_unitario * obj_speed) - ortogonal_wind

def actualizar_posicion():
    posicion_actual = np.copy(POSICION_INICIAL)
    velocidad_actual = 0.0
    tiempo_actual = 0.0
    energia = 0.0
    
    unit_vector, dist_total = get_vectors_unitarios(POSICION_INICIAL, POSICION_FINAL)
    norma_paralela, viento_ortogonal = decompose_wind(VIENTO, unit_vector)
    v_max = get_max_speed(POTENCIA_MAX, norma_paralela, ROZAMIENTO)
    
    # Vector de velocidad del aire (va) que el dron mantiene
    vector_va = navegator(viento_ortogonal, unit_vector, v_max)
    
    if vector_va is None:
        return "ERROR: El viento transversal es más fuerte que el dron."

    # Simulación
    dist_restante = np.linalg.norm(POSICION_FINAL - posicion_actual)
    
    while dist_restante > 0.0036: # Umbral de llegada
        if velocidad_actual != 0:
            fuerza_dron = min(F_MAX_ESTATICO, POTENCIA_MAX / velocidad_actual)
        else:
            fuerza_dron = F_MAX_ESTATICO
            
        fuerza_rozamiento = actualizar_fuerza_rozamiento(v_max) # Basado en velocidad aire
        
        # Simplificación de aceleración en el eje de progreso
        aceleracion_actual = (fuerza_dron - (fuerza_rozamiento + PESO)) / MASA
        
        velocidad_actual += aceleracion_actual * DELTA_T
        # La velocidad respecto al suelo es la suma del vector aire + viento
        v_suelo = vector_va + VIENTO
        
        # Actualizamos posición usando el vector de velocidad resultante
        posicion_actual += v_suelo * DELTA_T
        
        energia += fuerza_dron * velocidad_actual * DELTA_T
        tiempo_actual += DELTA_T
        dist_restante = np.linalg.norm(POSICION_FINAL - posicion_actual)
        
        print(posicion_actual, dist_restante,velocidad_actual, tiempo_actual, energia)
        
actualizar_posicion()
        
import numpy as np
import plotly.graph_objects as go

# # --- Constantes ---
# MASA = 15
# GRAVEDAD = 9.81
# PESO = GRAVEDAD * MASA
# ROZAMIENTO = 0.15
# POTENCIA_MAX = 3000
# POSICION_INICIAL = np.array([0.0, 0.0, 0.0])
# POSICION_FINAL = np.array([80.0, 50.0, 60.0])
# VIENTO = np.array([5.0, -2.0, 0.0])
# DELTA_T = 0.001
# F_MAX_ESTATICO = 400

# # --- FUNCIONES FÍSICAS (Intactas) ---
# def get_vectors_unitarios(pos_inicial, pos_final):
#     vector = np.array(pos_final) - np.array(pos_inicial)
#     distancia = np.linalg.norm(vector)
#     if distancia == 0:
#         return np.zeros_like(vector), 0
#     return vector / distancia, distancia

# def decompose_wind(vel_viento, vector_unitario):
#     viento_vector = vel_viento
#     projection_scalar = np.dot(viento_vector, vector_unitario)
#     projection_vector = projection_scalar * vector_unitario
#     ortogonal_wind = viento_vector - projection_vector
#     return projection_scalar, ortogonal_wind

# def actualizar_fuerza_rozamiento(velocidad_relativa):
#     return ROZAMIENTO * velocidad_relativa**2

# def get_max_speed(potencia_max, velocidad_viento, indice_rozamiento):
#     v_max = (potencia_max / indice_rozamiento)**(1/3)
#     return v_max

# def navegator(ortogonal_wind, vector_unitario, v_max):
#     norma_ortogonal = np.linalg.norm(ortogonal_wind)
#     if norma_ortogonal > v_max:
#         return None 
#     obj_speed = np.sqrt(v_max**2 - norma_ortogonal**2)
#     return (vector_unitario * obj_speed) - ortogonal_wind

# # --- SIMULACIÓN (Genera el historial de posiciones) ---
# def simular_vuelo():
#     posicion_actual = np.copy(POSICION_INICIAL)
#     velocidad_actual = 0.0
    
#     unit_vector, dist_total = get_vectors_unitarios(POSICION_INICIAL, POSICION_FINAL)
#     norma_paralela, viento_ortogonal = decompose_wind(VIENTO, unit_vector)
#     v_max = get_max_speed(POTENCIA_MAX, norma_paralela, ROZAMIENTO)
#     vector_va = navegator(viento_ortogonal, unit_vector, v_max)
    
#     if vector_va is None:
#         print("ERROR: El viento transversal es más fuerte que el dron.")
#         return []

#     dist_restante = np.linalg.norm(POSICION_FINAL - posicion_actual)
#     historial_posiciones = []
#     contador_iteraciones = 0
    
#     while dist_restante > 0.0036:
#         if velocidad_actual != 0:
#             fuerza_dron = min(F_MAX_ESTATICO, POTENCIA_MAX / velocidad_actual)
#         else:
#             fuerza_dron = F_MAX_ESTATICO
            
#         fuerza_rozamiento = actualizar_fuerza_rozamiento(v_max)
#         aceleracion_actual = (fuerza_dron - fuerza_rozamiento - PESO) / MASA
#         velocidad_actual += aceleracion_actual * DELTA_T
#         v_suelo = vector_va + VIENTO
#         posicion_actual += v_suelo * DELTA_T
#         dist_restante = np.linalg.norm(POSICION_FINAL - posicion_actual)
        
#         # Muestreo: Guardamos 1 de cada 100 cálculos para la animación
#         if contador_iteraciones % 100 == 0:
#             historial_posiciones.append(np.copy(posicion_actual))
            
#         contador_iteraciones += 1
        
#     historial_posiciones.append(np.copy(posicion_actual))
#     return np.array(historial_posiciones)

# # --- PIPELINE DE ANIMACIÓN EN PLOTLY ---
# def crear_animacion_plotly(historial):
#     if len(historial) == 0:
#         return

#     # 1. Definir los elementos estáticos (El escenario)
#     trazo_inicio = go.Scatter3d(
#         x=[POSICION_INICIAL[0]], y=[POSICION_INICIAL[1]], z=[POSICION_INICIAL[2]],
#         mode='markers', marker=dict(color='blue', size=5), name='Inicio (A)'
#     )
#     trazo_fin = go.Scatter3d(
#         x=[POSICION_FINAL[0]], y=[POSICION_FINAL[1]], z=[POSICION_FINAL[2]],
#         mode='markers', marker=dict(color='green', size=8, symbol='diamond'), name='Destino (B)'
#     )
#     trazo_ideal = go.Scatter3d(
#         x=[POSICION_INICIAL[0], POSICION_FINAL[0]], 
#         y=[POSICION_INICIAL[1], POSICION_FINAL[1]], 
#         z=[POSICION_INICIAL[2], POSICION_FINAL[2]],
#         mode='lines', line=dict(color='rgba(100,100,100,0.5)', dash='dash'), name='Ruta Ideal'
#     )

#     # 2. Definir los elementos dinámicos en su estado inicial (frame 0)
#     trazo_estela = go.Scatter3d(
#         x=[historial[0,0]], y=[historial[0,1]], z=[historial[0,2]],
#         mode='lines', line=dict(color='red', width=3), name='Trayectoria Real'
#     )
#     trazo_dron = go.Scatter3d(
#         x=[historial[0,0]], y=[historial[0,1]], z=[historial[0,2]],
#         mode='markers', marker=dict(color='red', size=6), name='Dron'
#     )

#     # 3. Construir los "Frames" (Fotogramas)
#     frames = []
#     # Plotly puede ponerse lento si hay demasiados frames, así que agrupamos un poco
#     paso_animacion = max(1, len(historial) // 150) 
    
#     for i in range(0, len(historial), paso_animacion):
#         # En Plotly, cada frame actualiza los datos de los trazos existentes.
#         # Solo actualizamos el trazo 3 (estela) y el 4 (dron).
#         frame_data = [
#             go.Scatter3d(x=historial[:i+1, 0], y=historial[:i+1, 1], z=historial[:i+1, 2]), # Actualiza estela
#             go.Scatter3d(x=[historial[i, 0]], y=[historial[i, 1]], z=[historial[i, 2]])     # Actualiza dron
#         ]
#         frames.append(go.Frame(data=frame_data, traces=[3, 4], name=str(i)))

#     # Aseguramos que el último frame exacto esté incluido
#     frames.append(go.Frame(
#         data=[
#             go.Scatter3d(x=historial[:, 0], y=historial[:, 1], z=historial[:, 2]),
#             go.Scatter3d(x=[historial[-1, 0]], y=[historial[-1, 1]], z=[historial[-1, 2]])
#         ], traces=[3, 4]
#     ))

#     # 4. Configurar el Layout (Caja 3D y botones)
#     layout = go.Layout(
#         title='Simulación 3D: Navegación del Dron con Viento',
#         scene=dict(
#             xaxis=dict(range=[0, 100], title='Eje X (m)'),
#             yaxis=dict(range=[-20, 60], title='Eje Y (m)'), # Margen negativo por el viento cruzado
#             zaxis=dict(range=[0, 80], title='Eje Z (m)'),
#             aspectmode='cube' # Mantiene la proporción visual cuadrada
#         ),
#         updatemenus=[dict(
#             type="buttons",
#             showactive=False,
#             buttons=[
#                 dict(label="▶ Reproducir",
#                      method="animate",
#                      args=[None, dict(frame=dict(duration=30, redraw=True), fromcurrent=True)]),
#                 dict(label="⏸ Pausar",
#                      method="animate",
#                      args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate", transition=dict(duration=0))])
#             ],
#             x=0.1, y=0.1, xanchor="right", yanchor="top"
#         )]
#     )

#     # 5. Ensamblar la figura y renderizarla
#     fig = go.Figure(
#         data=[trazo_inicio, trazo_fin, trazo_ideal, trazo_estela, trazo_dron], 
#         layout=layout, 
#         frames=frames
#     )
    
#     # Esto abrirá tu navegador web por defecto con la animación interactiva
#     fig.show()

# # Ejecución
# print("Calculando simulación física...")
# datos_vuelo = simular_vuelo()
# print("Generando entorno 3D en el navegador...")
# crear_animacion_plotly(datos_vuelo)