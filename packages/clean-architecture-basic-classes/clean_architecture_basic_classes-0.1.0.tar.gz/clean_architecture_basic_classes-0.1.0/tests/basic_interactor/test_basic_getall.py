from unittest.mock import MagicMock

from clean_architecture_basic_classes.basic_interactors.basic_get_all import \
    BasicGetAllRequestModel
from tests.basic_interactor.fixtures import (
    FakeAdapter,
    make_context
)
from clean_architecture_basic_classes.basic_interactors import \
    BasicGetAllInteractor


def test_basic_getall():
    fake_db = {}
    adapter = FakeAdapter(fake_db)
    entidades = make_context(adapter)

    request = BasicGetAllRequestModel(None)
    interactor = BasicGetAllInteractor(request, adapter_instance=adapter)
    resultado = interactor.run()

    assert len(resultado.object_list) == 3
    assert resultado.object_list[0]['nome'] in [x[0] for x in entidades]


def mock_entity(nome):
    return MagicMock(to_json=MagicMock(return_value={'nome': nome}))


def test_basic_getall_filter():
    fake_db = {}
    adapter = FakeAdapter(fake_db)
    make_context(adapter)
    adapter.filter = MagicMock(return_value=[
        mock_entity('siclano')
    ])

    params = dict(filter_field='nome', filter_value='siclano')
    request = BasicGetAllRequestModel(params)
    interactor = BasicGetAllInteractor(request, adapter_instance=adapter)
    resultado = interactor.run()

    assert len(resultado.object_list) == 1
    assert resultado.object_list[0]['nome'] == 'siclano'


def test_basic_getall_sort_asc():
    fake_db = {}
    adapter = FakeAdapter(fake_db)
    make_context(adapter)
    adapter.filter = MagicMock(return_value=[
        mock_entity('beltrano'),
        mock_entity('fulano'),
        mock_entity('siclano'),
    ])

    params = dict(sort_field='nome', sort_order='ASC')
    request = BasicGetAllRequestModel(params)
    interactor = BasicGetAllInteractor(request, adapter_instance=adapter)
    resultado = interactor.run()

    assert len(resultado.object_list) == 3
    assert resultado.object_list[0]['nome'] == 'wilson'


def test_basic_getall_sort_desc():
    fake_db = {}
    adapter = FakeAdapter(fake_db)
    make_context(adapter)
    adapter.filter = MagicMock(return_value=[
        mock_entity('siclano'),
        mock_entity('fulano'),
        mock_entity('beltrano')
    ])

    params = dict(sort_field='nome', sort_order='DESC')
    request = BasicGetAllRequestModel(params)
    interactor = BasicGetAllInteractor(request, adapter_instance=adapter)
    resultado = interactor.run()

    assert len(resultado.object_list) == 3
    assert resultado.object_list[0]['nome'] == 'yankee'


def test_get_sort_key():
    mock_request = MagicMock(sort_field='campo')
    mock_adapter = MagicMock()
    interactor = BasicGetAllInteractor(mock_request, mock_adapter)

    mock_object = MagicMock(campo=42)
    # noinspection PyProtectedMember
    result = interactor._get_sort_key(mock_object)

    assert result == 42


def test_get_sort_key_drill_down():
    mock_request = MagicMock(sort_field='campo_dot_subcampo')
    mock_adapter = MagicMock()
    interactor = BasicGetAllInteractor(mock_request, mock_adapter)

    mock_object = MagicMock(campo=MagicMock(subcampo=17))
    # noinspection PyProtectedMember
    result = interactor._get_sort_key(mock_object)

    assert result == 17


def test_basic_getall_paginated():
    fake_db = {}
    adapter = FakeAdapter(fake_db)
    entidades = make_context(adapter, 26)

    params = dict(pagination_perPage=5, pagination_page=1)
    request = BasicGetAllRequestModel(params)
    interactor = BasicGetAllInteractor(request, adapter_instance=adapter)
    resultado = interactor.run()

    assert len(resultado.object_list) == 5
    assert resultado.object_list[0]['nome'] == entidades[0][0]
    assert resultado.object_list[4]['nome'] == entidades[4][0]

    params = dict(pagination_perPage=5, pagination_page=2)
    request2 = BasicGetAllRequestModel(params)
    interactor2 = BasicGetAllInteractor(request2, adapter_instance=adapter)
    resultado2 = interactor2.run()

    assert len(resultado.object_list) == 5
    assert resultado2.object_list[0]['nome'] == entidades[5][0]
    assert resultado2.object_list[4]['nome'] == entidades[9][0]
