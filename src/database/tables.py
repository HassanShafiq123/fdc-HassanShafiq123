from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(3000))
    ingredients: Mapped[str] = mapped_column(Text)
    allergens: Mapped[str] = mapped_column(Text, nullable=True)
    picture: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    restraunt: Mapped[int] = mapped_column(ForeignKey("restraunt.id"), nullable=True)


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300))


class Restraunt(Base):
    __tablename__ = "restraunt"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300))
