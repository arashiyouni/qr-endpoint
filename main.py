from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import qrcode
import crud, models, db_schema
from database import engine, SessionLocal

# Inicializar las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint 1: Generar código QR
@app.get("/qr/{endpoint}")
def generar_qr(endpoint: str):
    url = f"http://localhost:8000/{endpoint}"
    img = qrcode.make(url)
    img.save("qr_code.png")
    return FileResponse("qr_code.png", media_type="image/png")

# Endpoint 2: Registrar asistencia
@app.post("/registrar", response_model=db_schema.RegistroAsistenciaResponse)
def registrar_asistencia(data: db_schema.RegistroAsistenciaBase, db: Session = Depends(get_db)):
    registro = crud.registrar_asistencia(db, data.id_evento, data.id_estudiante)
    if not registro:
        raise HTTPException(status_code=400, detail="Error al registrar asistencia")
    return registro

# Endpoint 3: Marcar como presente
@app.put("/marcar-presente", response_model=db_schema.RegistroAsistenciaResponse)
def marcar_presente(data: db_schema.RegistroAsistenciaBase, db: Session = Depends(get_db)):
    registro = crud.marcar_presente(db, data.id_evento, data.id_estudiante)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro
