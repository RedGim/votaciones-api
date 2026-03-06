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


@router.post("/voters")
def create_voter(voter: schemas.VoterCreate, db: Session = Depends(get_db)):

    existing_email = db.query(models.Voter).filter(
        models.Voter.email == voter.email
    ).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Ya existe un votante con ese email")

    existing = db.query(models.Candidate).filter(
        models.Candidate.name == voter.name
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Este usuario ya es candidato")

    new_voter = models.Voter(
        name=voter.name,
        email=voter.email
    )

    db.add(new_voter)
    db.commit()
    db.refresh(new_voter)

    return new_voter


@router.get("/voters")
def get_voters(db: Session = Depends(get_db)):
    return db.query(models.Voter).all()


@router.delete("/voters/{id}")
def delete_voter(id: int, db: Session = Depends(get_db)):

    voter = db.query(models.Voter).filter(models.Voter.id == id).first()

    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado")

    if voter.has_voted:
        raise HTTPException(status_code=400, detail="El votante ya votó, no se puede eliminar")

    db.delete(voter)
    db.commit()

    return {"message": "Votante eliminado"}
