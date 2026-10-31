# Sistema difuso Mamdani - Congestión vehicular (Puerta 1, UNT)

## Archivos
- `fuzzy_system.py` — define el sistema difuso (universos, funciones de
  membresía, base de reglas) y las funciones `evaluar()` / `categorizar()`.
- `app.py` — app web en Streamlit (interfaz para ingresar flujo/velocidad
  y obtener la congestión estimada).
- `requirements.txt` — dependencias para desplegar.
- `generar_figuras.py` — genera las figuras del paper (membresía y matriz
  de confusión) a partir del dataset.
- `datos_trafico_unt.csv` — dataset original (48 observaciones).
- `datos_con_prediccion.csv` — dataset con la salida del sistema añadida.
- `subset_diseno.csv` / `subset_evaluacion.csv` — split 70/30 estratificado.
- `fig_membresia.pdf/png`, `fig_matriz_confusion.pdf/png` — figuras listas
  para insertar en el LaTeX (usar las .pdf, son vectoriales).
- `screenshot_app.png` — evidencia de la app corriendo localmente.

## Cómo correr localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Cómo desplegar en Streamlit Community Cloud (gratis)
1. Sube esta carpeta a un repositorio de GitHub (puede ser público o
   privado, pero público es más simple para compartir el link).
2. Entra a https://share.streamlit.io con tu cuenta de GitHub.
3. "New app" → selecciona el repo → archivo principal: `app.py`.
4. Deploy. En 1-2 minutos tendrás una URL pública tipo
   `https://tuapp.streamlit.app` — esa es la evidencia de despliegue en
   la nube que pide la rúbrica (captura de pantalla + link).
