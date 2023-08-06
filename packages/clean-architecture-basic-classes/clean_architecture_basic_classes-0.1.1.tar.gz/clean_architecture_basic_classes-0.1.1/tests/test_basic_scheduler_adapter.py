from datetime import datetime

from pytest import fixture

from clean_architecture_basic_classes.basic_scheduler_adapter import \
    BasicTaskSchedulerAdapter


@fixture
def adapter_factory():
    def factory(mock_name=None,
                mock_identifier=None,
                mock_execution_time=None,
                mock_memory=None):
        class DummyAdapter(BasicTaskSchedulerAdapter):
            memory = mock_memory if mock_memory is not None else {}

            def __init__(self, name, identifier, execution_time):
                super().__init__(name, identifier, execution_time)

            def set(self):
                DummyAdapter.memory.update({self.name: self})

            def update(self):
                DummyAdapter.memory.update({self.name: self})

            def delete(self):
                del DummyAdapter.memory[self.name]

            @classmethod
            def get_current(cls, name: str):
                return cls.memory[name]

        instance = DummyAdapter(mock_name or 'task',
                                mock_identifier or 'action',
                                mock_execution_time or datetime(2030, 1, 1))
        return instance

    return factory


def test_basic_scheduler_adapter_set(adapter_factory):
    mock_name = 'task_name'
    mock_identifier = 'command_action'
    mock_event_time = datetime(2020, 8, 13, 7, 15)
    adapter = adapter_factory(mock_name, mock_identifier, mock_event_time)
    adapter.set()

    assert adapter.execution_time == mock_event_time
    assert adapter.name == mock_name
    assert adapter.identifier == mock_identifier


def test_basic_scheduler_adapter_update(adapter_factory):
    mock_name = 'task_name'
    mock_identifier = 'command_action'
    mock_event_time = datetime(2020, 8, 13, 7, 15)
    mock_mem = {}
    adapter = adapter_factory(mock_name,
                              mock_identifier,
                              mock_event_time,
                              mock_mem)
    adapter.set()

    assert mock_mem[mock_name].execution_time == mock_event_time

    mock_new_event_time = datetime(2021, 9, 14, 8, 16)
    adapter.execution_time = mock_new_event_time
    adapter.update()

    assert mock_mem[mock_name].execution_time == mock_new_event_time


def test_basic_scheduler_adapter_delete(adapter_factory):
    mock_mem = {}
    mock_name = 'test_delete'
    mock_event_time = datetime(2020, 8, 13, 7, 15)
    adapter = adapter_factory(mock_name=mock_name,
                              mock_memory=mock_mem,
                              mock_execution_time=mock_event_time)
    adapter.set()

    assert mock_name in mock_mem

    adapter.delete()

    assert mock_name not in mock_mem


def test_basic_scheduler_adapter_get_current(adapter_factory):
    memory = {}
    mock_event_time = datetime(2020, 8, 13, 7, 15)
    adapter = adapter_factory(mock_name='meu task',
                              mock_memory=memory,
                              mock_execution_time=mock_event_time)
    adapter.set()

    assert adapter.execution_time == mock_event_time

    loaded = adapter.get_current('meu task')

    assert loaded.execution_time == mock_event_time
