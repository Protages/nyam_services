from abc import ABC, abstractmethod


class BaseAbcRepo(ABC):
    '''Contains base CRUD methods that must be implemented in each repository.'''

    @abstractmethod
    async def get_by_id():
        raise NotImplementedError
    
    @abstractmethod
    async def get_all():
        raise NotImplementedError
    
    @abstractmethod
    async def update():
        raise NotImplementedError
    
    @abstractmethod
    async def create():
        raise NotImplementedError
    
    @abstractmethod
    async def delete():
        raise NotImplementedError
