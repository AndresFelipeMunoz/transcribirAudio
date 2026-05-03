from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import create_user, authenticate_user
from app.core.security import create_access_token
from app.db.session import SessionLocal

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        result = create_user(db, user.username, user.email, user.password)
        if isinstance(result, tuple):
            db_user, error = result
            if db_user is None:
                raise HTTPException(status_code=400, detail=error)
            return UserResponse.model_validate(db_user) 
        return UserResponse.model_validate(result)       
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}