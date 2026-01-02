
import pandas as pd
import numpy as np

# Constants from app.py
SMMLV_2025 = 1430000
AUX_TRANS_2025 = 175000
UVT_2025 = 49799
TOPE_EFECTIVO = 100 * UVT_2025
BASE_RET_SERVICIOS = 4 * UVT_2025
BASE_RET_COMPRAS = 27 * UVT_2025

def calcular_costo_empresa_fila(row, col_salario, col_aux, col_arl, col_exo):
    """Calculadora de Nómina Real - VERSIÓN DETALLADA"""
    try:
        salario = float(row[col_salario]) if pd.notnull(row[col_salario]) else 0
    except:
        salario = 0

    tiene_aux = str(row[col_aux]).strip().lower() in ['si', 's', 'true', '1', 'yes']

    # ARL
    if col_arl and col_arl in row and pd.notnull(row[col_arl]):
        try: nivel_arl = int(row[col_arl])
        except: nivel_arl = 1
    else: nivel_arl = 1

    es_exonerado = str(row[col_exo]).strip().lower() in ['si', 's', 'true', '1', 'yes']

    # --- CÁLCULOS DETALLADOS ---
    aux_trans = AUX_TRANS_2025 if tiene_aux else 0
    ibc = salario
    base_prest = salario + aux_trans

    # 1. SEGURIDAD SOCIAL (Empleador)
    salud = 0 if es_exonerado else ibc * 0.085
    pension = ibc * 0.12
    arl_t = {1:0.00522, 2:0.01044, 3:0.02436, 4:0.0435, 5:0.0696}
    arl_val = ibc * arl_t.get(nivel_arl, 0.00522)

    total_seg_social = salud + pension + arl_val

    # 2. PARAFISCALES
    paraf = ibc * 0.04 # Caja
    if not es_exonerado: paraf += ibc * 0.05 # SENA + ICBF

    # 3. PRESTACIONES SOCIALES (Prima, Cesantías, Int, Vacaciones)
    # Factor 21.83% sobre salario + auxilio
    total_prestaciones = base_prest * 0.2183

    # TOTAL COSTO
    costo_total = base_prest + total_seg_social + paraf + total_prestaciones

    # Retornamos los valores separados
    return costo_total, total_seg_social, total_prestaciones, paraf

def test_fix_bug():
    print("Running verification test for bug fix...")
    row = {"Salario": 1000000, "Aux": "Si", "ARL": 1, "Exo": "No"}
    try:
        # Simulate the NEW calling pattern
        costo_total, total_seg, total_prest, paraf = calcular_costo_empresa_fila(row, "Salario", "Aux", "ARL", "Exo")
        total_aportes = total_seg + total_prest + paraf
        print(f"Test PASSED: Unpacked successfully. Costo: {costo_total}, Aportes: {total_aportes}")
        assert costo_total > 1000000
    except ValueError as e:
        print(f"Test FAILED: Unpacking error: {e}")
    except Exception as e:
        print(f"Test FAILED: Unexpected error: {e}")

def analizar_gasto_fila(row, col_valor, col_metodo, col_concepto):
    """
    Evalúa una fila de gastos contables para detectar incumplimientos del Art 771-5
    y bases de retención en la fuente.
    """
    hallazgos = []
    riesgo = "BAJO"

    # Extracción segura de valores
    valor = float(row[col_valor]) if pd.notnull(row[col_valor]) else 0
    metodo = str(row[col_metodo]) if pd.notnull(row[col_metodo]) else ""

    # 1. Validación de Bancarización
    if 'efectivo' in metodo.lower() and valor > TOPE_EFECTIVO:
        hallazgos.append(f"⛔ RECHAZO FISCAL: Pago en efectivo (${valor:,.0f}) supera tope Art 771-5.")
        riesgo = "ALTO"

    # 2. Validación de Bases de Retención
    if valor >= BASE_RET_SERVICIOS and valor < BASE_RET_COMPRAS:
        hallazgos.append("⚠️ ALERTA: Verificar Retención (Base Servicios).")
        if riesgo == "BAJO": riesgo = "MEDIO"
    elif valor >= BASE_RET_COMPRAS:
        hallazgos.append("⚠️ ALERTA: Verificar Retención (Base Compras).")
        if riesgo == "BAJO": riesgo = "MEDIO"

    return " | ".join(hallazgos) if hallazgos else "OK", riesgo

def test_optimization_vectorization():
    print("\nRunning verification test for optimization (apply vs loop)...")
    # Simulate data
    data = {
        'Valor': [5000000, 200000, 10000000],
        'Metodo': ['Efectivo', 'Banco', 'Efectivo'],
        'Concepto': ['A', 'B', 'C']
    }
    df = pd.DataFrame(data)

    # OLD WAY (Loop) - simulated logic
    res_loop = []
    for r in df.to_dict('records'):
        h, rs = analizar_gasto_fila(r, 'Valor', 'Metodo', 'Concepto')
        res_loop.append((h, rs))

    # NEW WAY (Apply)
    df['val_check_safe'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
    def wrapper(row):
        return analizar_gasto_fila(row, 'Valor', 'Metodo', 'Concepto')

    analisis_result = df.apply(wrapper, axis=1)
    res_apply = list(zip(analisis_result.apply(lambda x: x[0]), analisis_result.apply(lambda x: x[1])))

    if res_loop == res_apply:
        print("Test PASSED: Vectorized logic matches loop logic.")
    else:
        print("Test FAILED: Results mismatch.")
        print("Loop:", res_loop)
        print("Apply:", res_apply)

if __name__ == "__main__":
    test_fix_bug()
    test_optimization_vectorization()
