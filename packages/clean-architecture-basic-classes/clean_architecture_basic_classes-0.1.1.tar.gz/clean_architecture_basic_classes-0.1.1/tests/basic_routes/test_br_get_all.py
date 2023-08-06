from unittest.mock import MagicMock, patch

from marshmallow import ValidationError
from pytest import raises

from clean_architecture_basic_classes.basic_routes.basic_routes import \
    BasicEntityRoutes
from clean_architecture_basic_classes.basic_routes.exceptions import \
    ValidationErrorException, UnexpectedErrorException


class Patches:
    pkg_prefix = 'clean_architecture_basic_classes.basic_routes.basic_routes'
    GetAllRequest = f'{pkg_prefix}.BasicGetAllRequestModel'
    GetAllInteractor = f'{pkg_prefix}.BasicGetAllInteractor'


@patch(Patches.GetAllRequest)
@patch(Patches.GetAllInteractor)
def test_ber_get_all(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    mock_query = MagicMock()
    mock_unit = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)
    result = ber.get_all(mock_query, mock_unit)

    mock_req.assert_called_with(mock_query, mock_unit)
    mock_inter.assert_called_with(mock_req.return_value, mock_adapter)
    mock_inter.return_value.run.assert_called_once()
    assert result == mock_inter.return_value.run.return_value


@patch(Patches.GetAllRequest)
@patch(Patches.GetAllInteractor, return_value=MagicMock(
    run=MagicMock(side_effect=ValidationError('oops'))))
def test_ber_get_all_validate_error(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    mock_query = MagicMock()
    mock_unit = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    with raises(ValidationErrorException) as excinfo:
        ber.get_all(mock_query, mock_unit)

    assert 'Erro de validação obtendo lista de' in str(excinfo.value)


@patch(Patches.GetAllRequest)
@patch(Patches.GetAllInteractor, return_value=MagicMock(
    run=MagicMock(side_effect=ValueError('Errado!'))))
def test_ber_get_all_general_error(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    mock_query = MagicMock()
    mock_unit = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    with raises(UnexpectedErrorException) as excinfo:
        ber.get_all(mock_query, mock_unit)

    assert 'Erro obtendo lista de' in str(excinfo.value)
    assert 'Errado!' in str(excinfo.value)
    assert 'ValueError' in str(excinfo.value)
