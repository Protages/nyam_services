from abc import ABC, abstractmethod

from src.repositories.courier.abstract import CourierAbcRepo


class UOWBaseAbc(ABC):
    '''
    Context manager. Base unit of work absract class. Use example:
    ```
    async with self.uow:
        res_1: SomeSchema1 = await self.uow.<SOME_REPO_1>.create(data_1)
        res_2: SomeSchema2 = await self.uow.<SOME_REPO_2>.create(data_2)
        await self.uow.commit()
    ```

    Both this repo will use one session.
    '''

    courier_repo: type[CourierAbcRepo]

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError
    
    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError
    
    @abstractmethod
    async def commit(self):
        raise NotImplementedError
    
    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
