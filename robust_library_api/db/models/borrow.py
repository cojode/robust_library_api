from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Date

from robust_library_api.db.base import Base

class BorrowModel(Base):
    __tablename__ = "borrow"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book_id: Mapped[str] = mapped_column(ForeignKey("book.id"))
    reader_name: Mapped[str] = mapped_column(String(length=200))
    date_of_issue: Mapped[date] = mapped_column(Date())
    date_of_return: Mapped[date] = mapped_column(Date(), nullable=True)