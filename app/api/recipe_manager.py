from typing import Annotated, Optional
from fastapi import Depends
from pydantic import TypeAdapter
from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user_manager import UserManager
from app.exceptions import NotAutorized
from app.models.base import get_fapi_db
from app.models.recipe import Recipe
from app.schemas.recipe import SRecipeDemo


class RecipeManager:
    def __init__(
        self,
        session: AsyncSession,
        user_manager: Optional[UserManager],
    ) -> None:
        self.session = session
        self.user_manager = user_manager

    async def get_all_recipes(self) -> list[SRecipeDemo]:
        query = (
            select(Recipe).options(joinedload(Recipe.user)).order_by(Recipe.created_at)
        )
        result = (await self.session.execute(query)).scalars().all()
        adapted = TypeAdapter(list[SRecipeDemo]).validate_python(result)
        return adapted

    async def add_new_recipe(self, description: str) -> Recipe:
        if self.user_manager is None:
            raise NotAutorized()
        user = await self.user_manager.get_user()
        query = (
            insert(Recipe)
            .values(description=description, user_id=user.tech_id)
            .returning(Recipe)
        )
        result = (await self.session.execute(query)).scalar_one()
        await self.session.commit()
        return result


def get_recipe_manager(
    session: Annotated[AsyncSession, Depends(get_fapi_db)],
    user_email: Optional[str] = None,
) -> RecipeManager:
    user_manager = None
    if user_email is not None:
        user_manager = UserManager(user_email, session)
    return RecipeManager(session, user_manager)
