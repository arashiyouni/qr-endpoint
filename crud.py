from sqlalchemy.orm import Session
from models import RegistroAsistencia

def registrar_asistencia(db: Session, id_evento: int, id_estudiante: int):
    registro = RegistroAsistencia(id_evento=id_evento, id_estudiante=id_estudiante)
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro

def marcar_presente(db: Session, id_evento: int, id_estudiante: int):
    registro = db.query(RegistroAsistencia).filter_by(id_evento=id_evento, id_estudiante=id_estudiante).first()
    if registro:
        registro.estado = "presente"
        db.commit()
        db.refresh(registro)
    return registro
