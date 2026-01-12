# Guía de Despliegue en la Web (Producción)

Al haber migrado de Streamlit (monolito) a Next.js + FastAPI (Arquitectura Moderna), **ya no puedes usar Streamlit Cloud** para desplegar toda la aplicación.
Necesitas desplegar el Frontend y el Backend por separado (o usar Docker).

Aquí tienes la estrategia recomendada "Premium":

## Opción 1: Git Push (La forma estándar)
Si ya tienes tu repositorio conectado a servicios como Vercel o Render, solo necesitas guardar y subir los cambios:

```bash
# 1. Verificar archivos modificados
git status

# 2. Agregar TODO lo nuevo (Backend y Frontend)
git add .

# 3. Guardar la versión
git commit -m "Migración Completa: Next.js + FastAPI + Módulos Premium"

# 4. Subir a la nube (GitHub/GitLab)
git push origin main
```

---

## Opción 2: Despliegue Manual (Paso a paso)

### 1. Frontend (Next.js) -> Vercel
Vercel es la casa de Next.js. Es gratis para hobby y muy rápido.

1.  Instala Vercel CLI: `npm i -g vercel`
2.  En la terminal, ve a la carpeta frontend:
    ```bash
    cd frontend
    vercel
    ```
3.  Sigue los pasos en pantalla (Enter, Enter...).
4.  ¡Listo! Te dará una URL tipo `proyecto-contador.vercel.app`.

### 2. Backend (FastAPI) -> Render / Railway
Necesitas un servidor para Python. Render.com es excelente.

1.  Crea un nuevo servicio en Render/Railway conectado a tu repo.
2.  Configura el **Root Directory** en `backend`.
3.  **Build Command**: `pip install -r ../requirements.txt`
4.  **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`

---

## Opción 3: Docker (Avanzado)
Si prefieres un contenedor todo en uno (no recomendado para serverless pero útil para VPS).

Crea un `Dockerfile` en la raíz (ya incluido en el proyecto base, pero necesita adaptarse para dual-stack o usar docker-compose).

Recomendamos **Opción 1 y 2** para la mejor escalabilidad y capa gratuita.
