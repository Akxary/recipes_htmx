from datetime import timezone, datetime
from enum import Enum
import logging
from typing import Annotated
from fastapi import Depends, Form
from sqlalchemy import insert, select, update
from app.api.utils import get_current_time
from app.models.base import get_fapi_db
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from resources.config import (
    SEND_CODE_LIMIT,
    SESSION_TIME_LIMIT,
    VERIFICATION_CODE_LIMIT,
)

logger = logging.getLogger(__name__)


class VerificationResult(Enum):
    INCORRECT_CODE = 1
    TIMEOUT = 2
    SUCCESS = 3


error_code_map: dict[VerificationResult, str] = {
    VerificationResult.INCORRECT_CODE: "Введен некорректный код",
    VerificationResult.TIMEOUT: "Время действия кода истекло",
}


class UserManager:
    def __init__(self, user_email: str, session: AsyncSession) -> None:
        self.user_email = user_email
        self.session = session

    async def get_user(self) -> User:
        query = select(User).filter(User.user_email == self.user_email)
        result = (await self.session.execute(query)).scalar_one_or_none()
        if result is None:
            return await self.create_user()
        return result

    async def create_user(self) -> User:
        query = insert(User).values(user_email=self.user_email).returning(User)
        result = (await self.session.execute(query)).scalar_one()
        await self.session.commit()
        return result

    async def set_verification_code(self, verification_code: int) -> User:
        query = (
            update(User)
            .where(User.user_email == self.user_email)
            .values(
                {
                    "verification_code": verification_code,
                    "verification_time": get_current_time(),
                }
            )
            .returning(User)
        )
        result = (await self.session.execute(query)).scalar_one()
        await self.session.commit()
        return result

    async def check_send_code_limit(self) -> datetime:
        user = await self.get_user()
        return user.verification_time.replace(tzinfo=timezone.utc) + SEND_CODE_LIMIT

    async def check_verification_code(
        self, verification_code: int
    ) -> VerificationResult:
        user = await self.get_user()
        current_time = get_current_time()
        user_verification_time = (
            user.verification_time.replace(tzinfo=timezone.utc)
            + VERIFICATION_CODE_LIMIT
        )
        logger.warning(
            "User verification time is %s, current time is %s",
            user_verification_time,
            current_time,
        )
        if user.verification_code != verification_code:
            return VerificationResult.INCORRECT_CODE
        if current_time > user_verification_time:
            return VerificationResult.TIMEOUT
        await self.activate_user_session()
        return VerificationResult.SUCCESS

    async def activate_user_session(self) -> User:
        query = (
            update(User)
            .where(User.user_email == self.user_email)
            .values({"active_time": get_current_time()})
            .returning(User)
        )
        logger.warning("Setting user %s active", self.user_email)
        result = (await self.session.execute(query)).scalar_one()
        await self.session.commit()
        return result

    async def check_user_session(self) -> bool:
        query = select(User).filter(User.user_email == self.user_email)
        user = (await self.session.execute(query)).scalar_one_or_none()
        if user is None:
            logger.warning("User with email %s does not exists", self.user_email)
            return False
        user_active_time = user.active_time + SESSION_TIME_LIMIT
        current_time = get_current_time()
        if current_time > user_active_time:
            logger.warning(
                "User %s session expired at %s", self.user_email, user_active_time
            )
            return False
        return True


def get_user_manager(
    session: Annotated[AsyncSession, Depends(get_fapi_db)],
    user_email: str = Form(...),
) -> UserManager:
    return UserManager(user_email, session)
