@echo off
echo ===================================================
echo   INICIANDO ASISTENTE CONTABLE PRO (Backend + Frontend)
echo ===================================================
echo.

echo 1. Iniciando Backend (FastAPI) en el puerto 8000...
start cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo 2. Iniciando Frontend (Next.js) en el puerto 3000...
start cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo   TODO LISTO!
echo   - Backend: http://localhost:8000 (API)
echo   - Frontend: http://localhost:3000 (Web)
echo ===================================================
echo   Si ves "Failed to fetch", espera 10 segundos a que el backend cargue.
echo.
pause
