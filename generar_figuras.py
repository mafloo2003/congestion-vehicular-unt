"""Genera las figuras para el capítulo de Resultados:
   1. Funciones de membresía (flujo, velocidad, congestión)
   2. Matriz de confusión (heatmap)
Guarda todo en formato PDF (vectorial, ideal para LaTeX) y PNG (preview).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from fuzzy_system import flujo, velocidad, congestion

plt.rcParams.update({'font.size': 9, 'font.family': 'serif'})

# ---------------------------------------------------------------------
# 1. Funciones de membresía
# ---------------------------------------------------------------------
fig, axs = plt.subplots(3, 1, figsize=(5, 6.5))

for label in flujo.terms:
    axs[0].plot(flujo.universe, flujo[label].mf, label=label, linewidth=1.6)
axs[0].set_title('Flujo vehicular (veh/min)')
axs[0].set_ylabel('Grado de pertenencia')
axs[0].legend(loc='upper right', fontsize=7)
axs[0].set_ylim(-0.02, 1.05)

for label in velocidad.terms:
    axs[1].plot(velocidad.universe, velocidad[label].mf, label=label, linewidth=1.6)
axs[1].set_title('Velocidad promedio (km/h)')
axs[1].set_ylabel('Grado de pertenencia')
axs[1].legend(loc='upper right', fontsize=7)
axs[1].set_ylim(-0.02, 1.05)

for label in congestion.terms:
    nombre = label.replace('_', ' ')
    axs[2].plot(congestion.universe, congestion[label].mf, label=nombre, linewidth=1.6)
axs[2].set_title('Congestión vehicular -- salida (0-100)')
axs[2].set_xlabel('Escala de salida')
axs[2].set_ylabel('Grado de pertenencia')
axs[2].legend(loc='upper right', fontsize=7)
axs[2].set_ylim(-0.02, 1.05)

plt.tight_layout()
plt.savefig('fig_membresia.pdf')
plt.savefig('fig_membresia.png', dpi=200)
plt.close()
print('fig_membresia.pdf / .png guardados')

# ---------------------------------------------------------------------
# 2. Matriz de confusión
# ---------------------------------------------------------------------
evaluacion = pd.read_csv('subset_evaluacion.csv')
labels = ['Bajo', 'Moderado', 'Alto', 'Muy alto']
cm = confusion_matrix(evaluacion['nivel_congestion_observado'],
                       evaluacion['categoria_predicha'], labels=labels)

fig, ax = plt.subplots(figsize=(4.2, 3.8))
im = ax.imshow(cm, cmap='Blues')
ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=30, ha='right')
ax.set_yticklabels(labels)
ax.set_xlabel('Nivel predicho por el sistema')
ax.set_ylabel('Nivel observado en campo')
for i in range(len(labels)):
    for j in range(len(labels)):
        color = 'white' if cm[i, j] > cm.max() / 2 else 'black'
        ax.text(j, i, str(cm[i, j]), ha='center', va='center', color=color, fontsize=10)
plt.tight_layout()
plt.savefig('fig_matriz_confusion.pdf')
plt.savefig('fig_matriz_confusion.png', dpi=200)
plt.close()
print('fig_matriz_confusion.pdf / .png guardados')
