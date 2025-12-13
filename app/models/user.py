from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import TIMESTAMP, Integer, String
from app.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.mixins import CreatedAtMixin, TechIdMixin

if TYPE_CHECKING:
    from app.models import Recipe


class User(Base, CreatedAtMixin, TechIdMixin):
    __tablename__ = "users"
    user_email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="email пользователя",
        index=True,
    )
    verification_code: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0",
        comment="Код подтверждения входа",
    )
    verification_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default="2000-01-01 00:00:00.000+00:00",
        comment="Время отправка кода подтверждения",
    )
    active_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        comment="Время активности пользователя",
    )
    recipes: Mapped[list["Recipe"]] = relationship(back_populates="user")
