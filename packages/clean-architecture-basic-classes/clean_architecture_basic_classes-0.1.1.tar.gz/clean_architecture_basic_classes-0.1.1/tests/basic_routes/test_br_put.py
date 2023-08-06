from unittest.mock import MagicMock, patch

from marshmallow import ValidationError
from pytest import raises

from clean_architecture_basic_classes.basic_interactors import \
    UpdateEntityException
from clean_architecture_basic_classes.basic_routes.basic_routes import \
    BasicEntityRoutes
from clean_architecture_basic_classes.basic_routes.exceptions import (
    ValidationErrorException,
    UnexpectedErrorException, PutException)


class Patches:
    pkg_prefix = 'clean_architecture_basic_classes.basic_routes.basic_routes'
    PutRequest = f'{pkg_prefix}.BasicPutRequestModel'
    PutInteractor = f'{pkg_prefix}.BasicPutInteractor'


@patch(Patches.PutRequest)
@patch(Patches.PutInteractor)
def test_ber_put(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    result = ber.put('meu id', 'data')

    mock_req.assert_called_with('meu id', 'data')
    mock_inter.assert_called_with(mock_req.return_value,
                                  mock_adapter,
                                  mock_class)
    mock_inter.return_value.run.assert_called_once()
    assert result == mock_inter.return_value.run.return_value


@patch(Patches.PutRequest)
@patch(Patches.PutInteractor, return_value=MagicMock(
    run=MagicMock(side_effect=UpdateEntityException('gravou não'))))
def test_ber_put_exception(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    with raises(PutException) as exc_info:
        ber.put('meu id', 'data')

    assert 'Erro atualizando' in str(exc_info.value)
    assert 'gravou não' in str(exc_info.value)


@patch(Patches.PutRequest)
@patch(Patches.PutInteractor, return_value=MagicMock(
    run=MagicMock(side_effect=ValidationError('123inválido321'))))
def test_ber_put_validation_exception(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    with raises(ValidationErrorException) as exc_info:
        ber.put('meu id', 'data')

    assert 'Erro de validação atualizando' in str(exc_info.value)
    assert '123inválido321' in str(exc_info.value)


@patch(Patches.PutRequest)
@patch(Patches.PutInteractor, return_value=MagicMock(
    run=MagicMock(side_effect=ValueError('Oops!'))))
def test_ber_put_general_exception(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    with raises(UnexpectedErrorException) as exc_info:
        ber.put('meu id', 'data')

    assert 'Erro atualizando' in str(exc_info.value)
    assert 'Oops!' in str(exc_info.value)
    assert 'ValueError' in str(exc_info.value)
