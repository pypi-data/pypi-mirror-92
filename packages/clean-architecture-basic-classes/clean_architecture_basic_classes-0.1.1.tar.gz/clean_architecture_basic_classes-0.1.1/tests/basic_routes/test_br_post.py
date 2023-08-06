from unittest.mock import MagicMock, patch

from marshmallow import ValidationError
from pytest import raises

from clean_architecture_basic_classes.basic_interactors import \
    SaveEntityException
from clean_architecture_basic_classes.basic_routes.basic_routes import \
    BasicEntityRoutes
from clean_architecture_basic_classes.basic_routes.exceptions import (
    ValidationErrorException,
    UnexpectedErrorException,
    PostException)


class Patches:
    pkg_prefix = 'clean_architecture_basic_classes.basic_routes.basic_routes'
    PostRequest = f'{pkg_prefix}.BasicPostRequestModel'


@patch(Patches.PostRequest)
def test_ber_post(mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    with patch.object(BasicEntityRoutes,
                      '_instantiate_post_interactor') as mock:
        ber = BasicEntityRoutes(mock_adapter, mock_class)
        result = ber.post('data')

    mock_req.assert_called_with('data')
    mock.assert_called_with(mock_req.return_value)
    mock.return_value.run.assert_called_once()
    assert result == mock.return_value.run.return_value


@patch(Patches.PostRequest)
def test_ber_post_validate_error(mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()

    with patch.object(BasicEntityRoutes,
                      '_instantiate_post_interactor',
                      return_value=MagicMock(
                          run=MagicMock(
                              side_effect=ValidationError('oops')))):
        ber = BasicEntityRoutes(mock_adapter, mock_class)

        with raises(ValidationErrorException) as excinfo:
            ber.post('não importa')

    assert 'Erro de validação criando' in str(excinfo.value)
    assert 'oops' in str(excinfo.value)


@patch(Patches.PostRequest)
def test_ber_post_general_error(mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()

    with patch.object(BasicEntityRoutes,
                      '_instantiate_post_interactor',
                      return_value=MagicMock(
                          run=MagicMock(
                              side_effect=ValueError('Errado!')))):
        ber = BasicEntityRoutes(mock_adapter, mock_class)

        with raises(UnexpectedErrorException) as excinfo:
            ber.post('não importa')

    assert 'Erro criando' in str(excinfo.value)
    assert 'Errado!' in str(excinfo.value)
    assert 'ValueError' in str(excinfo.value)


@patch(Patches.PostRequest)
def test_ber_post_save_error(mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()

    ipi = '_instantiate_post_interactor'
    with patch.object(BasicEntityRoutes, ipi, return_value=MagicMock(
        run=MagicMock(
            side_effect=SaveEntityException('save error')))):
        ber = BasicEntityRoutes(mock_adapter, mock_class)

        with raises(PostException) as excinfo:
            ber.post('não importa')

    assert 'Erro gravando' in str(excinfo.value)
    assert 'save error' in str(excinfo.value)
