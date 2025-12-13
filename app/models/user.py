from datetime import datetime
from sqlalchemy import TIMESTAMP, Integer, String
from app.models.base import Base
from sqlalchemy.orm import MappedColumn, Mapped

from app.models.mixins import CreatedAtMixin, TechIdMixin


class User(Base, CreatedAtMixin, TechIdMixin):
    __tablename__ = "users"
    user_email: Mapped[str] = MappedColumn(
        String,
        nullable=False,
        comment="email пользователя",
        index=True,
    )
    verification_code: Mapped[int] = MappedColumn(
        Integer,
        nullable=False,
        server_default="0",
        comment="Код подтверждения входа",
    )
    verification_time: Mapped[datetime] = MappedColumn(
        TIMESTAMP,
        nullable=False,
        server_default="2000-01-01 00:00:00.000",
        comment="Время отправка кода подтверждения",
    )
    
