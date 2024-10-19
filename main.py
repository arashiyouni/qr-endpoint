import tempfile
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import qrcode
import crud, models, db_schema
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

# Inicializar las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Especifica explícitamente el origen del frontend
    allow_credentials=True,  # Permite cookies y encabezados de autorización
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Dependencia para la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint 1: Generar código QR con URL que incluye los parámetros necesarios
@app.get("/qr/{endpoint}")
def generar_qr(endpoint: str, id_evento: int, id_estudiante: int):
    url = f"https://bc28-190-150-197-40.ngrok-free.app/{endpoint}?id_evento={id_evento}&id_estudiante={id_estudiante}"
    img = qrcode.make(url)

    # Usar un archivo temporal para guardar la imagen
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        img.save(temp_file.name)
        return FileResponse(temp_file.name, media_type="image/png")

# Endpoint 2: Registrar asistencia usando query parameters
@app.get("/registrar", response_model=db_schema.RegistroAsistenciaResponse)
def registrar_asistencia(
    id_evento: int = Query(...), 
    id_estudiante: int = Query(...), 
    db: Session = Depends(get_db)
):
    # Verificar si ya existe un registro para el estudiante en este evento con estado 'registrado'
    registro_existente = (
        db.query(models.RegistroAsistencia)
        .filter_by(id_evento=id_evento, id_estudiante=id_estudiante, estado='registrado')
        .first()
    )

    if registro_existente:
        raise HTTPException(
            status_code=400, 
            detail="El estudiante ya está registrado en este evento."
        )

    # Si no existe, registrar al estudiante
    registro = crud.registrar_asistencia(db, id_evento, id_estudiante)
    if not registro:
        raise HTTPException(status_code=400, detail="Error al registrar asistencia")
    
    return registro

# Endpoint 3: Marcar como presente usando query parameters
@app.get("/marcar-presente", response_model=db_schema.RegistroAsistenciaResponse)
def marcar_presente(
    id_evento: int = Query(...), 
    id_estudiante: int = Query(...), 
    db: Session = Depends(get_db)
):
    registro = crud.marcar_presente(db, id_evento, id_estudiante)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro