from abc import ABC, abstractmethod
from datetime import datetime


class TaskNotFoundException(BaseException):
    pass


class BasicTaskSchedulerAdapter(ABC):
    def __init__(self,
                 name: str,
                 identifier: str,
                 execution_time: datetime):
        self.name = name
        self.identifier = identifier
        self.execution_time = execution_time

    @abstractmethod
    def set(self):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_current(cls, name: str):
        raise NotImplementedError
