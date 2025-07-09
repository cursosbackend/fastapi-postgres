from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from .crud import get_users
from .models import User



Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return get_users(db)


