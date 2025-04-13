from .database import SessionLocal

#Crea y cierra sesiones para conectarse a la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
