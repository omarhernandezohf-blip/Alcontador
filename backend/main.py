from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import sys
import os
import json

# Agregar el directorio actual al path para importar logic.py correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar lógica existente
# Nota: logic.py ya maneja la carga de secretos y configuración
try:
    import logic
except ImportError as e:
    print(f"Warning: Could not import logic.py. Error: {e}")
    logic = None

app = FastAPI(
    title="Asistente Contable Pro API",
    description="Backend API for Enterprise Accounting Suite",
    version="1.0.0"
)

# Configuración CORS para permitir peticiones desde el Frontend (Next.js)
origins = [
    "http://localhost:3000", # Next.js dev server
    "http://localhost:3001",
    "*" # Por ahora permitir todo para desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "system": "Asistente Contable Pro API v1.0"}

@app.get("/health")
def health_check():
    return {"status": "ok", "backend_logic": "loaded" if logic else "failed"}

# --- Endpoints de Prueba para verificar integración con Logic ---

class AIQuery(BaseModel):
    prompt: str
    user_plan: str = "FREE"
    email: Optional[str] = None

@app.post("/api/ai/consult")
def consult_ai(query: AIQuery):
    if not logic:
        raise HTTPException(status_code=500, detail="Logic module not loaded")
    
    # Simular créditos por ahora si no hay DB conectada
    response = logic.consultar_ia_gemini(
        prompt=query.prompt,
        user_plan=query.user_plan,
        credits=0, 
        email=query.email or ""
    )
    return {"response": response}

# --- Endpoints de Módulos Avanzados ---

@app.post("/api/xml/process")
async def process_xml_batch(files: List[UploadFile] = File(...)):
    if not logic: raise HTTPException(status_code=500, detail="Logic module error")
    
    processed_data = []
    
    for file in files:
        try:
            # Leer contenido del CSV/XML
            content = await file.read()
            # logic.parsear_xml_dian espera un objeto archivo o path,
            # pero aquí lo adaptaremos para leer desde bytes si es necesario
            # o guardamos temporalmente. 
            # Dado que logic.parsear_xml_dian usa ET.parse(archivo_xml),
            # podemos pasar un BytesIO.
            import io
            file_obj = io.BytesIO(content)
            # Hack para que logic.py pueda leer el atributo .name si lo usa
            file_obj.name = file.filename 
            
            result = logic.parsear_xml_dian(file_obj)
            processed_data.append(result)
        except Exception as e:
            processed_data.append({"Archivo": file.filename, "Error": str(e)})
            
    return {"data": processed_data}

class UGPPInput(BaseModel):
    salario: float
    no_salarial: float

@app.post("/api/ugpp/analyze")
def analyze_ugpp(input_data: UGPPInput):
    if not logic: raise HTTPException(500, "Logic not loaded")
    
    # Adaptar a la firma de logic.calcular_ugpp_fila(row, col_salario, col_no_salarial)
    # Creamos un dict dummy
    row = {'salario': input_data.salario, 'no_salarial': input_data.no_salarial}
    
    nuevo_ibc, exceso, riesgo, mensaje = logic.calcular_ugpp_fila(row, 'salario', 'no_salarial')
    
    return {
        "nuevo_ibc": nuevo_ibc,
        "exceso": exceso,
        "riesgo": riesgo,
        "mensaje": mensaje
    }

# --- Auditoría Fiscal ---

@app.post("/api/fiscal/audit")
async def audit_expenses(file: UploadFile = File(...)):
    if not logic: raise HTTPException(500, "Logic error")
    
    try:
        content = await file.read()
        import io
        
        # Detectar formato
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(content))
        else:
            df = pd.read_csv(io.BytesIO(content))
            
        results = []
        # Asumimos columnas estandar por ahora o las primeras encontradas
        # En una app real, el usuario mapearía las columnas. 
        # Intentamos adivinar:
        cols = df.columns.astype(str).str.lower()
        col_valor = next((c for c in df.columns if 'valor' in str(c).lower() or 'monto' in str(c).lower()), None)
        col_metodo = next((c for c in df.columns if 'metodo' in str(c).lower() or 'pago' in str(c).lower()), None)
        
        if not col_valor:
            return {"error": "No se encontró columna de Valor"}
            
        for _, row in df.iterrows():
            hallazgo, riesgo = logic.analizar_gasto_fila(row, col_valor, col_metodo, '')
            row_dict = row.to_dict()
            # Convert NaN to None per JSON standard
            row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
            
            results.append({
                **row_dict,
                "Hallazgo_IA": hallazgo,
                "Nivel_Riesgo": riesgo
            })
            
        return {"data": results}
    except Exception as e:
        return {"error": str(e)}

# --- Tesorería (Datos Proyectados) ---

@app.get("/api/treasury/projection")
def get_treasury_projection():
    # ... (código existente)
    # Simulación de datos complejos para gráficos
    # Generamos 12 meses de proyección
    data = []
    base_income = 50000000
    base_expense = 35000000
    
    for i in range(12):
        month_name = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"][i]
        income = base_income * (1 + (random.randint(-10, 20) / 100))
        expense = base_expense * (1 + (random.randint(-5, 15) / 100))
        cash_flow = income - expense
        
        data.append({
            "month": month_name,
            "ingresos": int(income),
            "egresos": int(expense),
            "flujo": int(cash_flow),
            "acumulado": int(cash_flow * (i+1)) # Simplificado
        })
        
    return {"projection": data}

import pandas as pd
import random

# --- Validador RUT ---

@app.get("/api/rut/calculate/{nit}")
def calculate_dv(nit: str):
    if not logic: raise HTTPException(500, "Logic error")
    dv = logic.calcular_dv_colombia(nit)
    return {"nit": nit, "dv": dv}

# --- OCR Facturas ---

@app.post("/api/ocr/scan")
async def scan_invoice(file: UploadFile = File(...)):
    if not logic: raise HTTPException(500, "Logic error")
    
    try:
        content = await file.read()
        # Simular delay para UX
        import asyncio
        await asyncio.sleep(2) 
        
        # logic.ocr_factura requiere bytes de imagen
        result = logic.ocr_factura(content) # Asume plan FREE por defecto en logic si no se pasa
        
        if result:
            return {"success": True, "data": result}
        else:
            return {"success": False, "error": "No se pudo extraer información legible"}
    except Exception as e:
        return {"success": False, "error": str(e)}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
