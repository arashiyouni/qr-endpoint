from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class Evento(Base):
    __tablename__ = "evento"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=False)

class Estudiante(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    carnet = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    university_carrer = Column(String(255), nullable=False)

class RegistroAsistencia(Base):
    __tablename__ = "registro_asistencias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_evento = Column(Integer, ForeignKey('evento.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    id_estudiante = Column(Integer, ForeignKey('students.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    estado = Column(Enum('registrado', 'presente'), default='registrado', nullable=False)
    fecha_registro = Column(TIMESTAMP, default=None)

    evento = relationship("Evento", backref="asistencias")
    estudiante = relationship("Estudiante", backref="asistencias")
