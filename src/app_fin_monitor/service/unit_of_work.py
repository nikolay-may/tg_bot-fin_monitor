from abc import ABC, abstractmethod

from app_fin_monitor.adapters.repository import SQLAlchemyRepository


class AbstractUnitOfWork(ABC):
    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        self.session_in_act = self.session()
        self.repo = SQLAlchemyRepository(self.session_in_act)
        return super().__aenter__()

    async def __aexit__(self, *args):
        super().__aexit__(*args)
        self.session_in_act.close()

    async def commit(self):
        await self.session_in_act.commit()

    async def rollback(self):
        await self.session_in_act.rollback()
