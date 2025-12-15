from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, String, false
from sqlalchemy.orm import Mapped, mapped_column
from app.api.utils import get_current_time
from app.models.base import Base
from app.models.mixins import CreatedAtMixin, TechIdMixin
from resources.config import REFRESH_TOKEN_LIMIT


class Token(Base, CreatedAtMixin, TechIdMixin):
    __tablename__ = "refresh_tokens"
    jit: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        comment="Уникальный ИД токена",
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tech_id"))
    token_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="Хеш токена",
    )
    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        comment="Время (utc) истечения токена",
        default_factory=lambda: get_current_time() + REFRESH_TOKEN_LIMIT,
    )
    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        server_default=false(),
        comment="Является ли токен отозванным",
    )
    user_agent: Mapped[str] = mapped_column(String, comment="Устройство выдачи токена")
