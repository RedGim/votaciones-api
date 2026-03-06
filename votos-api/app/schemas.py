from pydantic import BaseModel

class VoterCreate(BaseModel):
    name: str
    email: str


class CandidateCreate(BaseModel):
    name: str
    party: str


class VoteCreate(BaseModel):
    voter_id: int
    candidate_id: int
