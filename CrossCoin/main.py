import logging
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn
import crud
import models
import schemas
from database import SessionLocal, engine
from starlette.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error("Database connection error: %s", e)
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/collect/", response_model=schemas.User)
async def collect_coins(username: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        user = crud.create_user(db, username=username)
    user = crud.add_coins(db, user=user)
    return user


@app.get("/leaderboard/", response_model=list[schemas.User])
async def get_leaderboard(db: Session = Depends(get_db)):
    return crud.get_leaderboard(db)


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8066, reload=True, workers=3)
