from pydantic import BaseModel


class NumerologyRequest(BaseModel):
    dob: str
