# 🛑 LEÉME: CÓMO TERMINAR TU DESPLIEGUE

¡Hola! Dejamos todo preparado, pero faltaron 2 clics para que tu aplicación funcione en Internet.
Sigue estos pasos cuando regreses:

## Paso 1: Configurar Render (El paso crítico)

El error "Application exited early" ocurrió porque Render no sabía qué puerto usar.
Para arreglarlo:

1.  Entra a [dashboard.render.com](https://dashboard.render.com).
2.  Ve a tu servicio **`Alcontador`**.
3.  Pestaña **Settings** -> Busca **Start Command**.
4.  Dale a **Edit** y pon EXACTAMENTE esto:
    
    `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

5.  Dale a **Save Changes**.
6.  Render empezará a trabajar solo. Espera a que diga **"Live" 🟢**.

## Paso 2: Verificar Web

1.  Una vez Render esté en verde, ve a tu web: [https://asistente-contable-pro.vercel.app](https://asistente-contable-pro.vercel.app)
2.  Prueba el Login con:
    *   **User:** `suitmaxi@premium.com`
    *   **Pass:** `maxi54321`

---
**Nota Técnica:**
He actualizado el código (`backend/main.py`) para que maneje los puertos automáticamente, así que también soportará futuras configuraciones.
