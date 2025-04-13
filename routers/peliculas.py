from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import PeliculaDB, modelPelicula
from DB.conexion import get_db

router = APIRouter(prefix="/peliculas", tags=["Películas CRUD"])

@router.post("/")
def agregar_pelicula(pelicula: modelPelicula, db: Session = Depends(get_db)):
    db_pelicula = db.query(PeliculaDB).filter(PeliculaDB.Titulo == pelicula.Titulo).first()
    if db_pelicula:
        raise HTTPException(status_code=400, detail="La película ya está registrada.")
    nueva = PeliculaDB(**pelicula.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {"mensaje": f"Película '{nueva.Titulo}' registrada exitosamente.", "pelicula": pelicula}

@router.get("/")
def consultar_todas(db: Session = Depends(get_db)):
    return db.query(PeliculaDB).all()

@router.get("/{titulo}")
def consultar_pelicula(titulo: str, db: Session = Depends(get_db)):
    pelicula = db.query(PeliculaDB).filter(PeliculaDB.Titulo == titulo).first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada.")
    return pelicula

@router.put("/{titulo}")
def editar_pelicula(titulo: str, datos_actualizados: modelPelicula, db: Session = Depends(get_db)):
    pelicula = db.query(PeliculaDB).filter(PeliculaDB.Titulo == titulo).first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada.")
    pelicula.Titulo = datos_actualizados.Titulo
    pelicula.Genero = datos_actualizados.Genero
    pelicula.año = datos_actualizados.año
    pelicula.Clasificacion = datos_actualizados.Clasificacion
    db.commit()
    return {"mensaje": f"Película '{titulo}' actualizada correctamente."}

@router.delete("/{titulo}")
def eliminar_pelicula(titulo: str, db: Session = Depends(get_db)):
    pelicula = db.query(PeliculaDB).filter(PeliculaDB.Titulo == titulo).first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada.")
    db.delete(pelicula)
    db.commit()
    return {"mensaje": f"Película '{titulo}' eliminada correctamente."}
