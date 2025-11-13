from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Conexión con SQLite ---
DATABASE_URL = "sqlite:///./library.db"

# Para SQLite se requiere este parámetro especial
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# --- Dependencia para inyección en FastAPI ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
