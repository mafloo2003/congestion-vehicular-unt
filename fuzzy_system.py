"""
Sistema de inferencia difusa Mamdani para evaluar la congestión vehicular
en la Puerta 1 de la Universidad Nacional de Trujillo (UNT).

Variables:
  - flujo_vehicular (veh/min)   -> Bajo, Medio, Alto
  - velocidad_promedio (km/h)   -> Baja, Media, Alta
  - congestion_vehicular (0-100, salida crisp tras defuzzificación)
       conjuntos linguisticos internos: Bajo, Moderado, Alto, Muy alto

Base de reglas: la misma Tabla I ya presentada en Entrega 1 (9 reglas,
3 flujo x 3 velocidad).
"""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ---------------------------------------------------------------------
# 1. Universos de discurso (definidos a partir de los rangos reales
#    observados en campo: flujo 5.1-49.7 veh/min, velocidad 8.7-54.4 km/h)
# ---------------------------------------------------------------------
flujo = ctrl.Antecedent(np.arange(0, 56, 0.1), 'flujo_vehicular')
velocidad = ctrl.Antecedent(np.arange(0, 61, 0.1), 'velocidad_promedio')
congestion = ctrl.Consequent(np.arange(0, 101, 0.1), 'congestion_vehicular')

# ---------------------------------------------------------------------
# 2. Funciones de membresía (triangulares y trapezoidales)
# ---------------------------------------------------------------------
# Flujo vehicular (veh/min)
flujo['Bajo'] = fuzz.trapmf(flujo.universe, [0, 0, 10, 20])
flujo['Medio'] = fuzz.trimf(flujo.universe, [10, 22, 34])
flujo['Alto'] = fuzz.trapmf(flujo.universe, [25, 35, 56, 56])

# Velocidad promedio (km/h) -- a mayor velocidad, menor congestión
velocidad['Baja'] = fuzz.trapmf(velocidad.universe, [0, 0, 15, 28])
velocidad['Media'] = fuzz.trimf(velocidad.universe, [18, 30, 42])
velocidad['Alta'] = fuzz.trapmf(velocidad.universe, [32, 45, 61, 61])

# Congestión vehicular (salida, 0-100)
congestion['Bajo'] = fuzz.trapmf(congestion.universe, [0, 0, 15, 35])
congestion['Moderado'] = fuzz.trimf(congestion.universe, [20, 40, 60])
congestion['Alto'] = fuzz.trimf(congestion.universe, [45, 65, 85])
congestion['Muy_alto'] = fuzz.trapmf(congestion.universe, [70, 85, 100, 100])

# ---------------------------------------------------------------------
# 3. Base de reglas (idéntica a la Tabla I de Entrega 1)
# ---------------------------------------------------------------------
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

congestion_ctrl = ctrl.ControlSystem(rules)


def evaluar(flujo_veh, velocidad_prom):
    """Devuelve el valor crisp (0-100) de congestión vehicular."""
    sim = ctrl.ControlSystemSimulation(congestion_ctrl)
    sim.input['flujo_vehicular'] = flujo_veh
    sim.input['velocidad_promedio'] = velocidad_prom
    sim.compute()
    return sim.output['congestion_vehicular']


def categorizar(valor_crisp):
    """Mapea el valor crisp (0-100) a una de las 4 categorías lingüísticas,
    usando los centros/picos de los conjuntos de salida como fronteras
    de decisión (método de 'máxima pertenencia esperada')."""
    if valor_crisp < 27.5:
        return 'Bajo'
    elif valor_crisp < 50:
        return 'Moderado'
    elif valor_crisp < 72.5:
        return 'Alto'
    else:
        return 'Muy alto'


if __name__ == '__main__':
    # Prueba rápida con un caso de cada categoría
    casos = [
        (8.5, 46.2, 'Bajo'),
        (21.0, 33.2, 'Moderado'),
        (26.8, 23.7, 'Alto'),
        (45.0, 15.5, 'Muy alto'),
    ]
    for f, v, esperado in casos:
        crisp = evaluar(f, v)
        cat = categorizar(crisp)
        print(f'flujo={f:5.1f} vel={v:5.1f} -> crisp={crisp:6.2f} -> {cat:9s} (esperado: {esperado})')
