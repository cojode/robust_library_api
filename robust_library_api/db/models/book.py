from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Integer

from robust_library_api.db.base import Base


class BookModel(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(length=200))
    description: Mapped[str] = mapped_column(String(length=1024))
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    remaining_amount: Mapped[int] = mapped_column(Integer())
