from fastapi import HTTPException, status


class NotAutorized(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "user not authorized"

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)
