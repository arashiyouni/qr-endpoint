from pydantic import BaseModel

class RegistroAsistenciaBase(BaseModel):
    id_evento: int
    id_estudiante: int

class RegistroAsistenciaResponse(BaseModel):
    id: int
    estado: str

    class Config:
        orm_mode = True
