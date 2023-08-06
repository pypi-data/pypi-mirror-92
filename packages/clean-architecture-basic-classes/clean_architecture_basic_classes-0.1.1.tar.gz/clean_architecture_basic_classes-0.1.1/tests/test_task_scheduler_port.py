from clean_architecture_basic_classes.basic_domain.task_scheduler_port import \
    TaskSchedulerPort
from pytest import fixture
from unittest.mock import MagicMock


@fixture
def consumer_factory():
    def factory():
        class AdapterConsumer(TaskSchedulerPort):
            def __init__(self):
                super().__init__()

        return AdapterConsumer()

    return factory


def test_task_scheduler_port(consumer_factory):
    consumer = consumer_factory()

    assert consumer.scheduler_adapter is None

    mock_adapter = MagicMock()
    consumer.set_scheduler_adapter(mock_adapter)

    assert consumer.scheduler_adapter == mock_adapter
