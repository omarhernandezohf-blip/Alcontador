@echo off
echo ==================================================
echo      ASISTENTE CONTABLE PRO - INICIANDO...
echo ==================================================

echo 1. Verificando entorno Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado. Por favor instala Python y asegúrate de agregar al PATH.
    pause
    exit /b
)

echo 2. Instalando dependencias faltantes...
echo    - Python libs...
python -m pip install -r requirements.txt
echo    - Node modules...
cd frontend
if not exist node_modules call npm install
cd ..

echo 3. Iniciando Servicios...

:: Start Backend
start "Backend API (Python)" cmd /k "python -m uvicorn backend.main:app --reload"

:: Start Frontend
cd frontend
start "Frontend Web (Next.js)" cmd /k "npm run dev"

:: Start Streamlit
cd ..
start "Legacy App (Streamlit)" cmd /k "python -m streamlit run app.py"

echo. 
echo [EXITO] Todos los sistemas iniciados.
echo - Web Nueva: http://localhost:3000
echo - Backend: http://localhost:8000
echo - Streamlit: http://localhost:8501
echo.
echo No cierres las ventanas negras que aparecieron.
pause
