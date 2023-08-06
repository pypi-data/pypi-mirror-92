from abc import ABC

from clean_architecture_basic_classes.basic_scheduler_adapter import \
    BasicTaskSchedulerAdapter


class TaskSchedulerPort(ABC):
    def __init__(self):
        self.scheduler_adapter = None

    def set_scheduler_adapter(self,
                              scheduler_adapter: BasicTaskSchedulerAdapter):
        self.scheduler_adapter = scheduler_adapter
