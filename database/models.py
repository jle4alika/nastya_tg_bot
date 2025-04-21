from sqlalchemy import BigInteger, String, Float, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import random

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    group: Mapped[int] = mapped_column(BigInteger, default=0)


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    faculty: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(), default='', unique=True)
    headman: Mapped[int] = mapped_column(BigInteger)
    deputy: Mapped[int] = mapped_column(BigInteger, default=0)
    members: Mapped[int] = mapped_column(Integer(), default=0)
    homework: Mapped[str] = mapped_column(String(), default='')
    schedule: Mapped[str] = mapped_column(String(), default='')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def restart_bd():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)