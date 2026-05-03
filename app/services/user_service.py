from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password

def create_user(db: Session, username: str, email: str, password: str):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise ValueError("El nombre de usuario ya existe")
    
    if db.query(User).filter(User.email == email).first():
        return None, "El email ya existe"

    user = User(username=username, email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user