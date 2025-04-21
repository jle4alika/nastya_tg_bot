from database.models import async_session
from database.models import User, Group
from sqlalchemy import select, update, text, delete

async def get_user_bool(tg_id: int):
    async with async_session() as session:
        query = await session.execute(select(User).where(User.tg_id == tg_id))
        result = query.fetchall()
        return bool(len(result))


async def get_headman(group: str):
    async with async_session() as session:
        query = await session.scalar(select(Group.headman).where(Group.name == group))
        return int(query)


async def get_group_headman(tg_id: int):
    async with async_session() as session:
        group = await session.scalar(select(User.group).where(User.tg_id == tg_id))
        query = await session.scalar(select(Group.headman).where(Group.headman == group))
        return query


async def get_group_deputy(tg_id: int):
    async with async_session() as session:
        group = await session.scalar(select(User.group).where(User.tg_id == tg_id))
        query = await session.scalar(select(Group.deputy).where(Group.headman == group))
        return query


# async def get_all_names(tg_id: int):
#     async with async_session() as session:
#         query = await session.scalars(select(User.name).where(User.tg_id != tg_id))
#         result = query.fetchall()
#         return result

async def get_homework(tg_id: int):
    async with async_session() as session:
        group = await session.scalar(select(User.group).where(User.tg_id == tg_id))
        query = await session.scalar(select(Group.homework).where(Group.headman == group))
        return str(query)

async def group_schedule(tg_id: int):
    async with async_session() as session:
        group = await session.scalar(select(User.group).where(User.tg_id == tg_id))
        query = await session.scalar(select(Group.schedule).where(Group.headman == group))
        return str(query)

async def get_group_members(tg_id: int):
    async with async_session() as session:
        query = await session.scalar(select(Group.members).where(Group.headman == tg_id))
        return int(query)

async def get_groups():
    async with async_session() as session:
        query = await session.scalars(select(Group.headman))
        result = query.fetchall()
        return result

async def get_group_title(tg_id: int):
    async with async_session() as session:
        group = await session.scalar(select(User.group).where(User.tg_id == tg_id))
        query = await session.scalar(select(Group.name).where(Group.headman == group))
        return query


async def get_groups_titles():
    async with async_session() as session:
        query = await session.scalars(select(Group.name))
        result = query.fetchall()
        return result


async def get_group_users(group: int):
    async with async_session() as session:
        query = await session.scalars(select(User.tg_id).where(User.group == group))
        result = query.fetchall()
        return result

async def get_user_group(tg_id: int):
    async with async_session() as session:
        group = await session.scalar(select(User.group).where(User.tg_id == tg_id))
        return group