from datetime import datetime
from sqlalchemy import TIMESTAMP, Integer
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import Mapped, MappedColumn


class TechIdMixin:
    tech_id: Mapped[int] = MappedColumn(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Технический ИД таблицы",
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = MappedColumn(
        TIMESTAMP,
        nullable=False,
        onupdate=current_timestamp(),
        comment="Время последнего обновления записи",
    )


class CreatedAtMixin:
    created_at: Mapped[datetime] = MappedColumn(
        TIMESTAMP,
        nullable=False,
        server_default=current_timestamp(),
        comment="Время создания записи",
    )
