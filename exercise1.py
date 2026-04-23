import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN INICIAL ---
MASA = 15
GRAVEDAD = 9.81
PESO = GRAVEDAD * MASA
ROZAMIENTO = 0.1
ALTURA_OBJETIVO = 100
DELTA_T = 0.001
ENERGIA_MAX = 25000
POTENCIA_MAXIMA = 2500
F_MAX_ESTATICO = 400

def actualizar_fuerza_rozamiento(velocidad):
    return ROZAMIENTO * velocidad**2

def actualizar_posicion():
    # Inicialización de variables de estado
    posicion_actual = 0
    tiempo_actual = 0
    velocidad_actual = 0
    energia = 0
    
    # Listas para almacenar la historia de la simulación
    hist_t, hist_x, hist_v, hist_a, hist_e = [0], [0], [0], [0], [0]
        
    while posicion_actual < ALTURA_OBJETIVO:
        # Lógica de fuerza del dron (Límite por potencia)
        if velocidad_actual != 0:
            fuerza_dron = min(F_MAX_ESTATICO, POTENCIA_MAXIMA / velocidad_actual)
        else:
            fuerza_dron = F_MAX_ESTATICO
        
        fuerza_rozamiento = actualizar_fuerza_rozamiento(velocidad_actual)
        
        # Segunda Ley de Newton: a = F_neta / m
        aceleracion_actual = (fuerza_dron - PESO - fuerza_rozamiento) / MASA
        
        # Integración numérica (Método de Euler)
        velocidad = velocidad_actual + aceleracion_actual * DELTA_T        
        posicion = posicion_actual + velocidad * DELTA_T
        
        # Cálculo de energía (Trabajo = Fuerza * Velocidad * Delta_t)
        # Esto es equivalente a P * dt
        energia += fuerza_dron * velocidad_actual * DELTA_T

        # Actualización para el siguiente paso
        velocidad_actual = velocidad
        posicion_actual = posicion
        tiempo_actual += DELTA_T

        # Guardar en el historial
        hist_t.append(tiempo_actual)
        hist_x.append(posicion_actual)
        hist_v.append(velocidad_actual)
        hist_a.append(aceleracion_actual)
        hist_e.append(energia)

    # Retornamos todo el historial para graficar
    return hist_t, hist_x, hist_v, hist_a, hist_e

# --- 2. EJECUCIÓN Y RECOLECCIÓN DE DATOS ---
t, x, v, a, e = actualizar_posicion()

# --- 3. CREACIÓN DE GRÁFICOS ---
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Título principal en negrita
fig.suptitle(f"Simulacion Entrega paquete con {F_MAX_ESTATICO}", fontsize=16, fontweight='bold')

# Datos finales para los labels
t_f, x_f, v_f, a_f, e_f = t[-1], x[-1], v[-1], a[-1], e[-1]

# Gráfico 1: Posición vs Tiempo
axs[0, 0].plot(t, x, 'b-', linewidth=2)
axs[0, 0].set_title('Posición respecto al Tiempo')
axs[0, 0].set_ylabel('Altura (m)')
axs[0, 0].plot(t_f, x_f, 'ro', label=f'Llegada: {t_f:.2f}s')
axs[0, 0].legend(); axs[0, 0].grid(True)

# Gráfico 2: Velocidad vs Tiempo
axs[0, 1].plot(t, v, 'g-', linewidth=2)
axs[0, 1].set_title('Velocidad respecto al Tiempo')
axs[0, 1].set_ylabel('Velocidad (m/s)')
axs[0, 1].plot(t_f, v_f, 'ro', label=f'V final: {v_f:.2f} m/s')
axs[0, 1].legend(); axs[0, 1].grid(True)

# Gráfico 3: Aceleración vs Tiempo
axs[1, 0].plot(t, a, 'r-', linewidth=2)
axs[1, 0].set_title('Aceleración respecto al Tiempo')
axs[1, 0].set_ylabel('Aceleración (m/s²)')
axs[1, 0].plot(t_f, a_f, 'ro', label=f'A final: {a_f:.2f} m/s²')
axs[1, 0].legend(); axs[1, 0].grid(True)

# Gráfico 4: Energía vs Tiempo
axs[1, 1].plot(t, e, 'm-', linewidth=2)
axs[1, 1].set_title('Energía respecto al Tiempo')
axs[1, 1].set_ylabel('Energía (Joules)')
axs[1, 1].plot(t_f, e_f, 'ro', label=f'E total: {e_f:.2f} J')
# Línea de referencia del límite de energía
axs[1, 1].axhline(y=ENERGIA_MAX, color='black', linestyle='--', label='Límite Energía')
axs[1, 1].legend(); axs[1, 1].grid(True)

plt.subplots_adjust(top=0.9, hspace=0.3)
plt.show()

# Verificación final por consola
if e_f < ENERGIA_MAX:
    print(f"Éxito: Se gastaron {e_f:.2f}J (Límite: {ENERGIA_MAX}J)")
else:
    print(f"Fallo: Se gastaron {e_f:.2f}J (Excede el límite)")
