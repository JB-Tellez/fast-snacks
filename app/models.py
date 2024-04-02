from pydantic import BaseModel

class Snack(BaseModel):
    name: str
    description: str
    
