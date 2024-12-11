from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Date

from robust_library_api.db.base import Base


class AuthorModel(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=200))
    surname: Mapped[str] = mapped_column(String(length=200))
    birth_date: Mapped[date] = mapped_column(Date())
