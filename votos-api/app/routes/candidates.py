from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
import app.models as models
import app.schemas as schemas


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/candidates")
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):

    existing_voter = db.query(models.Voter).filter(
        models.Voter.name == candidate.name
    ).first()

    if existing_voter:
        raise HTTPException(status_code=400, detail="Este usuario ya es votante, no puede ser candidato")

    existing_candidate = db.query(models.Candidate).filter(
        models.Candidate.name == candidate.name
    ).first()

    if existing_candidate:
        raise HTTPException(status_code=400, detail="Ya existe un candidato con ese nombre")

    new_candidate = models.Candidate(
        name=candidate.name,
        party=candidate.party
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate


@router.get("/candidates")
def get_candidates(db: Session = Depends(get_db)):

    return db.query(models.Candidate).all()
