from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
import app.models as models
import app.schemas as schemas
import pandas as pd
import matplotlib.pyplot as plt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/votes")
def vote(vote: schemas.VoteCreate, db: Session = Depends(get_db)):

    voter = db.query(models.Voter).filter(models.Voter.id == vote.voter_id).first()

    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado")

    if voter.has_voted:
        raise HTTPException(status_code=400, detail="El votante ya votó")

    candidate = db.query(models.Candidate).filter(
        models.Candidate.id == vote.candidate_id
    ).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    new_vote = models.Vote(
        voter_id=vote.voter_id,
        candidate_id=vote.candidate_id
    )

    voter.has_voted = True
    candidate.votes += 1

    db.add(new_vote)
    db.commit()

    return {"message": "Voto registrado"}


@router.get("/votes")
def get_votes(db: Session = Depends(get_db)):

    return db.query(models.Vote).all()


@router.get("/votes/statistics")
def statistics(db: Session = Depends(get_db)):

    candidates = db.query(models.Candidate).all()

    names = []
    votes = []

    for c in candidates:
        names.append(c.name)
        votes.append(c.votes)

    data = {
        "candidate": names,
        "votes": votes
    }

    df = pd.DataFrame(data)

    df.plot(x="candidate", y="votes", kind="bar")

    plt.title("Resultados de votación")
    plt.savefig("votes_chart.png")

    return data
