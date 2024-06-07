from typing import List
from datetime import date
from sqlalchemy import String, ForeignKey, Float, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Stoks(Base):
    __tablename__ = "stoks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_stok: Mapped[str] = mapped_column(String(150), nullable=False)
    purchase_price: Mapped[float] = mapped_column(Float)
    purchase_date: Mapped[date] = mapped_column(Date)

    stok_price_movments = relationship("StokPriceMovment", back_populates="stoks")


class StokPriceMovment(Base):
    __tablename__ = "stok_price_movment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stok_id: Mapped[List] = mapped_column(ForeignKey("stoks.id"), nullable=False)
    closing_price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    closing_date: Mapped[Date] = mapped_column(Date, nullable=False)
