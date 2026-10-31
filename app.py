"""
App web -- Sistema difuso Mamdani para evaluar la congestión vehicular
en la Puerta 1 de la UNT.

Despliegue: Streamlit Community Cloud (streamlit.io/cloud).
Ejecución local:  streamlit run app.py
"""
import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

st.set_page_config(page_title="Congestión Vehicular - Puerta 1 UNT", page_icon="🚦")

# ---------------------------------------------------------------------
# Sistema difuso (misma definición que fuzzy_system.py)
# ---------------------------------------------------------------------
@st.cache_resource
def construir_sistema():
    flujo = ctrl.Antecedent(np.arange(0, 56, 0.1), 'flujo_vehicular')
    velocidad = ctrl.Antecedent(np.arange(0, 61, 0.1), 'velocidad_promedio')
    congestion = ctrl.Consequent(np.arange(0, 101, 0.1), 'congestion_vehicular')

    flujo['Bajo'] = fuzz.trapmf(flujo.universe, [0, 0, 10, 20])
    flujo['Medio'] = fuzz.trimf(flujo.universe, [10, 22, 34])
    flujo['Alto'] = fuzz.trapmf(flujo.universe, [25, 35, 56, 56])

    velocidad['Baja'] = fuzz.trapmf(velocidad.universe, [0, 0, 15, 28])
    velocidad['Media'] = fuzz.trimf(velocidad.universe, [18, 30, 42])
    velocidad['Alta'] = fuzz.trapmf(velocidad.universe, [32, 45, 61, 61])

    congestion['Bajo'] = fuzz.trapmf(congestion.universe, [0, 0, 15, 35])
    congestion['Moderado'] = fuzz.trimf(congestion.universe, [20, 40, 60])
    congestion['Alto'] = fuzz.trimf(congestion.universe, [45, 65, 85])
    congestion['Muy_alto'] = fuzz.trapmf(congestion.universe, [70, 85, 100, 100])

    rules = [
        ctrl.Rule(flujo['Bajo'] & velocidad['Alta'], congestion['Bajo']),
        ctrl.Rule(flujo['Bajo'] & velocidad['Media'], congestion['Bajo']),
        ctrl.Rule(flujo['Bajo'] & velocidad['Baja'], congestion['Moderado']),
        ctrl.Rule(flujo['Medio'] & velocidad['Alta'], congestion['Bajo']),
        ctrl.Rule(flujo['Medio'] & velocidad['Media'], congestion['Moderado']),
        ctrl.Rule(flujo['Medio'] & velocidad['Baja'], congestion['Alto']),
        ctrl.Rule(flujo['Alto'] & velocidad['Alta'], congestion['Moderado']),
        ctrl.Rule(flujo['Alto'] & velocidad['Media'], congestion['Alto']),
        ctrl.Rule(flujo['Alto'] & velocidad['Baja'], congestion['Muy_alto']),
    ]
    return ctrl.ControlSystem(rules)


def categorizar(valor_crisp):
    if valor_crisp < 27.5:
        return 'Bajo', '🟢'
    elif valor_crisp < 50:
        return 'Moderado', '🟡'
    elif valor_crisp < 72.5:
        return 'Alto', '🟠'
    else:
        return 'Muy alto', '🔴'


sistema = construir_sistema()

# ---------------------------------------------------------------------
# Interfaz
# ---------------------------------------------------------------------
st.title("🚦 Evaluación difusa de congestión vehicular")
st.caption("Puerta 1 - Universidad Nacional de Trujillo | Sistema de inferencia difusa tipo Mamdani")

col1, col2 = st.columns(2)
with col1:
    flujo_in = st.slider("Flujo vehicular (veh/min)", 0.0, 55.0, 25.0, 0.5)
with col2:
    velocidad_in = st.slider("Velocidad promedio (km/h)", 0.0, 60.0, 25.0, 0.5)

if st.button("Evaluar congestión", type="primary"):
    sim = ctrl.ControlSystemSimulation(sistema)
    sim.input['flujo_vehicular'] = flujo_in
    sim.input['velocidad_promedio'] = velocidad_in
    sim.compute()
    crisp = sim.output['congestion_vehicular']
    categoria, emoji = categorizar(crisp)

    st.metric("Congestión vehicular estimada (0-100)", f"{crisp:.1f}")
    st.subheader(f"{emoji} Nivel: {categoria}")
    st.progress(min(crisp / 100, 1.0))

    with st.expander("Ver superficie de salida del sistema"):
        fig, ax = plt.subplots(figsize=(5, 1.2))
        ax.barh([0], [crisp], color='steelblue')
        ax.set_xlim(0, 100)
        ax.set_yticks([])
        ax.set_xlabel("Escala de congestión (0-100)")
        st.pyplot(fig)

st.divider()
st.caption(
    "Proyecto grupal - Curso Inteligencia Artificial II (UNT). "
    "Sistema basado en reglas difusas Mamdani entrenadas con observaciones "
    "de campo en la Puerta 1 de la UNT (Ñ2026)."
)
