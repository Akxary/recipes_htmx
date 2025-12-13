from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String

from app.models.base import Base
from app.models.mixins import CreatedAtMixin, UpdatedAtMixin
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column, relationship

if TYPE_CHECKING:
    from app.models import User


class Recipe(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="Идентификатор рецепта"
    )
    description: Mapped[str] = mapped_column(
        String, nullable=False, comment="Описание рецепта"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tech_id"))
    user: Mapped["User"] = relationship(back_populates="recipes")
