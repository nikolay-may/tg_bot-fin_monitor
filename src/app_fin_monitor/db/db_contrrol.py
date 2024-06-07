from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    inspect,
    MetaData,
    Date,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config_reader import config
from db.models import Base, Stoks, StokPriceMovment


engine = create_async_engine(config.db_lite.get_secret_value(), echo=True)

sessionmaker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def show_all_table():
    async with engine.begin() as conn:
        table = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    return table


async def create_all_db():
    async with engine.begin() as conn:
        res = await conn.run_sync(Base.metadata.create_all)
        return res


async def drop_all_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_single_table(table_name):
    metadata = MetaData()
    table_st = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name_stok", String),
        Column("purchase_price", Float),
        Column("purchase_date", Date),
    )

    table_st_mv = Table(
        f"{table_name}_movment",
        metadata,
        Column("id", Integer, primary_key=True),
        Column(
            f"{table_name}.id", Integer, ForeignKey(f"{table_name}.id"), nullable=False
        ),
        Column("closing_price", Float),
        Column("closing_date", Date),
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_st.create, checkfirst=True)
        await conn.run_sync(table_st_mv.create, checkfirst=True)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Stoks.create, StokPriceMovment.create)
        await conn.run_sync(StokPriceMovment.create)
