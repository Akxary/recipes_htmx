from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SUserEmail(BaseModel):
    user_email: str
    model_config = ConfigDict(from_attributes=True)


class SRecipeDemo(BaseModel):
    id: int
    user: SUserEmail
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
