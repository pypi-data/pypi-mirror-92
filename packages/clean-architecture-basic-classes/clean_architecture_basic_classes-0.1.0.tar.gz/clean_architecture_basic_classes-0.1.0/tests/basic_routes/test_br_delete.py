from unittest.mock import MagicMock, patch

from pytest import raises

from clean_architecture_basic_classes.basic_routes.basic_routes import \
    BasicEntityRoutes
from clean_architecture_basic_classes.basic_routes.exceptions import (
    UnexpectedErrorException, NotFoundException)


class Patches:
    pkg_prefix = 'clean_architecture_basic_classes.basic_routes.basic_routes'
    DeleteRequest = f'{pkg_prefix}.BasicDeleteRequestModel'
    DeleteInteractor = f'{pkg_prefix}.BasicDeleteInteractor'


@patch(Patches.DeleteRequest)
@patch(Patches.DeleteInteractor)
def test_ber_delete(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    result = ber.delete('meu id')

    mock_req.assert_called_with('meu id')
    mock_inter.assert_called_with(mock_req.return_value,
                                  mock_adapter)
    mock_inter.return_value.run.assert_called_once()
    assert result == mock_inter.return_value.run.return_value


@patch(Patches.DeleteRequest)
@patch(Patches.DeleteInteractor, return_value=MagicMock(
    run=MagicMock(return_value=None)))
def test_ber_delete_not_found(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    with raises(NotFoundException) as exc_info:
        ber.delete('meu id')

    assert 'não encontrado para ser deletado' in str(exc_info.value)


@patch(Patches.DeleteRequest)
@patch(Patches.DeleteInteractor, return_value=MagicMock(
    run=MagicMock(side_effect=ValueError('Oops!'))))
def test_ber_delete_general_exception(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)

    with raises(UnexpectedErrorException) as exc_info:
        ber.delete('meu id')

    assert 'Erro removendo' in str(exc_info.value)
    assert 'Oops!' in str(exc_info.value)
    assert 'ValueError' in str(exc_info.value)
