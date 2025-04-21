from database.models import async_session
from database.models import User, Group
from sqlalchemy import select, update, text, delete

import datetime

async def set_user(tg_id: int, referrer_id=None) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            if referrer_id != None:
                session.add(User(tg_id=tg_id, group=referrer_id))
                await session.commit()
            else:
                session.add(User(tg_id=tg_id))
                await session.commit()
        else:
            if referrer_id != None:
                await session.execute(update(User).where(User.tg_id == tg_id).values(group=referrer_id))
                await session.commit()
async def set_user_group(tg_id: int, group: int) -> None:
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(group=group))
        await session.commit()

async def set_group(tg_id: int, name: str, faculty: str) -> None:
    async with async_session() as session:
        group = await session.scalar(select(Group).where(Group.headman == tg_id))

        if not group:
            session.add(Group(headman=tg_id, faculty=faculty, name=name))
            await session.commit()
