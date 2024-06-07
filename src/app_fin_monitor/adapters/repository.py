from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy import delete, select
from db import models


class AbstarctRepositorty(ABC):
    @abstractmethod
    def add(self, record: Dict[str, int]):
        raise NotImplementedError

    @abstractmethod
    def get(self, id_record: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstarctRepositorty):
    def __init__(self, session):
        self.session = session

    async def add(self, record):
        await self.session.add(record)

    async def get(self, id_record):
        res = await self.session.get(id_record)
        return res

    async def delete(self, name_stok):
        statment = delete(models.Stoks).where(models.Stoks.name_stok == name_stok)
        await self.session.execute(statment)

    async def list(self):
        statment = select(models.Stoks)
        res = await self.session.execute(statment)
        return res.scalars().all()
