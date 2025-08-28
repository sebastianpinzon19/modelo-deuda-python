from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from modelo_deuda import procesar_modelo_deuda
from procesador_anticipos import procesar_anticipos
from procesador_cartera import procesar_cartera
from procesador_unificado import ProcesadorCarteraUnificado
from trm_config import load_trm, save_trm

# ================================
# Configuración inicial
# ================================
app = FastAPI(title="Backend Grupo Planeta", version="1.0.0")

# 🔹 Permitir conexión desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ En producción limitar al dominio PHP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta de salidas fijas
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "salidas")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================================
#        ENDPOINTS TRM
# ================================
@app.get("/trm")
def get_trm():
    """Obtener TRM actual"""
    return load_trm()

@app.post("/trm")
def post_trm(data: dict):
    """Actualizar TRM"""
    usd = data.get("usd")
    eur = data.get("eur")
    path = save_trm(usd, eur)
    return {"status": "ok", "path": path}

# ================================
#     ENDPOINT MODELO DEUDA
# ================================
@app.post("/procesar/modelo_deuda")
async def procesar_modelo(cartera: UploadFile, anticipos: UploadFile):
    try:
        path_cartera = os.path.join(OUTPUT_DIR, cartera.filename)
        path_anticipos = os.path.join(OUTPUT_DIR, anticipos.filename)
        out_path = os.path.join(OUTPUT_DIR, "modelo_deuda_resultado.xlsx")

        # Guardar archivos subidos
        with open(path_cartera, "wb") as f:
            shutil.copyfileobj(cartera.file, f)
        with open(path_anticipos, "wb") as f:
            shutil.copyfileobj(anticipos.file, f)

        # Cargar TRM
        trm = load_trm()

        # Procesar
        resultado = procesar_modelo_deuda(
            path_cartera,
            path_anticipos,
            trm.get("usd") or 0,
            trm.get("eur") or 0,
            out_path
        )

        return FileResponse(
            resultado,
            filename="modelo_deuda.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ================================
#     ENDPOINT ANTICIPOS
# ================================
@app.post("/procesar/anticipos")
async def procesar_anticipos_api(anticipos: UploadFile):
    try:
        path_anticipos = os.path.join(OUTPUT_DIR, anticipos.filename)

        # Guardar archivo
        with open(path_anticipos, "wb") as f:
            shutil.copyfileobj(anticipos.file, f)

        resultado = procesar_anticipos(path_anticipos)

        if not resultado:
            return JSONResponse(content={"error": "No se pudo procesar anticipos"}, status_code=400)

        return FileResponse(
            resultado,
            filename="anticipos.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ================================
#     ENDPOINT CARTERA
# ================================
@app.post("/procesar/cartera")
async def procesar_cartera_api(cartera: UploadFile, fecha_cierre: str = Form(None)):
    try:
        path_cartera = os.path.join(OUTPUT_DIR, cartera.filename)
        resultado_path = os.path.join(OUTPUT_DIR, "cartera.xlsx")

        # Guardar archivo
        with open(path_cartera, "wb") as f:
            shutil.copyfileobj(cartera.file, f)

        procesar_cartera(path_cartera, output_path=resultado_path, fecha_cierre_str=fecha_cierre)

        return FileResponse(
            resultado_path,
            filename="cartera.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ================================
#     ENDPOINT UNIFICADO
# ================================
@app.post("/procesar/unificado")
async def procesar_unificado_api(unificado: UploadFile):
    try:
        path_zip = os.path.join(OUTPUT_DIR, unificado.filename)

        # Guardar archivo
        with open(path_zip, "wb") as f:
            shutil.copyfileobj(unificado.file, f)

        proc = ProcesadorCarteraUnificado()
        resultado = proc.procesar_carpeta(OUTPUT_DIR)

        return FileResponse(
            resultado,
            filename="unificado.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
