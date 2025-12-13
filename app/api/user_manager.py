from datetime import timezone
import logging
from typing import Annotated
from fastapi import Depends, Form
from sqlalchemy import insert, select, update
from app.api.utils import get_current_time
from app.models.base import get_fapi_db
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from resources.config import VERIFICATION_CODE_LIMIT

logger = logging.getLogger(__name__)

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

    async def check_verification_code(self, verification_code: int) -> bool:
        user = await self.get_user()
        current_time = get_current_time()
        user_verification_time = user.verification_time.replace(tzinfo=timezone.utc) + VERIFICATION_CODE_LIMIT
        logger.warning("User verification time is %s, current time is %s", user_verification_time, current_time)
        return (
            user.verification_code == verification_code
            and current_time < user_verification_time
        )


def get_user_manager(
    session: Annotated[AsyncSession, Depends(get_fapi_db)],
    user_email: str = Form(...),
) -> UserManager:
    return UserManager(user_email, session)
