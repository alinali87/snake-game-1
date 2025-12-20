from typing import List

import models
import schemas
from database import engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers import auth
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Snake Game API")

# Include routers
app.include_router(auth.router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Snake Game API"}


@app.post("/api/scores", response_model=schemas.Score)
def create_score(score: schemas.ScoreCreate, db: Session = Depends(get_db)):
    db_score = models.Score(player_name=score.player_name, score=score.score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


@app.get("/api/scores", response_model=List[schemas.Score])
def get_scores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    scores = (
        db.query(models.Score)
        .order_by(models.Score.score.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return scores


@app.get("/api/scores/{score_id}", response_model=schemas.Score)
def get_score(score_id: int, db: Session = Depends(get_db)):
    score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    return score
