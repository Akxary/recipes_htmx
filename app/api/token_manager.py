

from abc import ABC, abstractmethod
from datetime import timedelta

from fastapi import Response
import jwt

from resources.config import ALGORITHM
class BaseToken(ABC):
    def __init__(self, token_name: str)->None:
        self.token_name = token_name
        self.max_age: timedelta
        self.salt: str = "salt"
        
    
    def generate_token(self, token_payload: dict) -> str:
        return jwt.encode(token_payload, self.salt, algorithm=ALGORITHM)
    
    def set_token(self, token: str, response: Response) -> None:
        response.set_cookie(
            self.token_name,
            value=token,
            max_age=int(self.max_age.total_seconds()),
            httponly=True,
            secure=True,
            samesite="strict",
        )

class TokenManager:
    pass