from unittest.mock import MagicMock

from pytest import raises

from clean_architecture_basic_classes.basic_interactors import (
    BasicPutInteractor,
    BasicPutRequestModel,
    UpdateEntityException)
from tests.basic_interactor.fixtures import (
    FakeAdapter,
    FakeEntity,
    make_context
)


def test_basic_put():
    fake_db = {}
    adapter = FakeAdapter(fake_db)
    make_context(adapter)

    entity_to_update = list(fake_db.values())[0]['entity_id']
    put_data = {'entity_id': entity_to_update,
                'nome': 'outro nome',
                'idade': 42}

    request = BasicPutRequestModel(entity_to_update, put_data)
    interactor = BasicPutInteractor(request, adapter, FakeEntity)

    result = interactor.run()

    assert result == dict(nome='outro nome',
                          idade=42,
                          entity_id=entity_to_update)

    assert fake_db[entity_to_update]['nome'] == 'outro nome'
    assert fake_db[entity_to_update]['idade'] == 42


def test_basic_put_fail():
    adapter = MagicMock(save=MagicMock(side_effect=Exception('oops')))

    put_data = {'entity_id': 'asdf',
                'nome': 'outro nome',
                'idade': 42}

    request = BasicPutRequestModel('asdf', put_data)
    interactor = BasicPutInteractor(request, adapter, FakeEntity)

    with raises(UpdateEntityException) as exc_info:
        interactor.run()

    assert 'Erro alterando entidade: oops' == str(exc_info.value)
