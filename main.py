from fastapi import FastAPI
from DB.database import Base, engine
from routers import peliculas

app = FastAPI(
    title="API de Películas - Examen Final Tercer Parcial",
    version="1.0"
)

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Incluir router
app.include_router(peliculas.router)

@app.get("/", tags=["Inicio"])
def home():
    return {"mensaje": "Bienvenido al Examen Final Tercer Parcial de Sergio Olmedo"}