from fastapi import FastAPI
from app.database import engine
import app.models as models
from app.routes import voters, candidates, votes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(voters.router)
app.include_router(candidates.router)
app.include_router(votes.router)
