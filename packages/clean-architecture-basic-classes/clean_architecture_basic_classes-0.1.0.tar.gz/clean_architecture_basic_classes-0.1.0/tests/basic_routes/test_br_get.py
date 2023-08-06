from unittest.mock import MagicMock, patch

from marshmallow import ValidationError
from pytest import raises

from clean_architecture_basic_classes.basic_routes.basic_routes import \
    BasicEntityRoutes
from clean_architecture_basic_classes.basic_routes.exceptions import (
    ValidationErrorException,
    UnexpectedErrorException,
    NotFoundException)


class Patches:
    pkg_prefix = 'clean_architecture_basic_classes.basic_routes.basic_routes'
    GetRequest = f'{pkg_prefix}.BasicGetRequestModel'
    GetInteractor = f'{pkg_prefix}.BasicGetInteractor'


@patch(Patches.GetRequest)
@patch(Patches.GetInteractor)
def test_ber_get(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)
    result = ber.get_by_id('meu id')

    mock_req.assert_called_with('meu id')
    mock_inter.assert_called_with(mock_req.return_value, mock_adapter)
    mock_inter.return_value.run.assert_called_once()
    assert result == mock_inter.return_value.run.return_value


@patch(Patches.GetRequest)
@patch(Patches.GetInteractor, return_value=MagicMock(
    run=MagicMock(side_effect=ValidationError('oops'))))
def test_ber_get_validate_error(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    with raises(ValidationErrorException) as excinfo:
        ber.get_by_id('não importa')

    assert 'Erro de validação obtendo' in str(excinfo.value)


@patch(Patches.GetRequest)
@patch(Patches.GetInteractor, return_value=MagicMock(
    run=MagicMock(side_effect=ValueError('Errado!'))))
def test_ber_get_general_error(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    with raises(UnexpectedErrorException) as excinfo:
        ber.get_by_id('não importa')

    assert 'Erro obtendo' in str(excinfo.value)
    assert 'Errado!' in str(excinfo.value)
    assert 'ValueError' in str(excinfo.value)


@patch(Patches.GetRequest)
@patch(Patches.GetInteractor, return_value=MagicMock(
    run=MagicMock(return_value=None)))
def test_ber_get_not_found(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    with raises(NotFoundException) as excinfo:
        ber.get_by_id('123asdf123')

    assert '123asdf123 não encontrado' in str(excinfo.value)
