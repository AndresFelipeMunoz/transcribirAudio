from app.db.base import Base
from app.db.session import engine

# 👇 IMPORTANTE: importar modelos
from app.models.user import User
from app.models.transcription import Transcription

print("Creando tablas...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas")