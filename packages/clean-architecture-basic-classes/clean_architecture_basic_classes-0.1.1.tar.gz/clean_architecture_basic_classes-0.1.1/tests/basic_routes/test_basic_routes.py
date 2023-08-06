from unittest.mock import MagicMock, patch

from clean_architecture_basic_classes.basic_routes.basic_routes import \
    BasicEntityRoutes


class Patches:
    pkg_prefix = 'clean_architecture_basic_classes.basic_routes.basic_routes'
    PostRequest = f'{pkg_prefix}.BasicPostRequestModel'
    PostInteractor = f'{pkg_prefix}.BasicPostInteractor'
    DeleteRequest = f'{pkg_prefix}.BasicDeleteRequestModel'
    DeleteInteractor = f'{pkg_prefix}.BasicDeleteInteractor'


def test_ber_object_name():
    mock_adapter = MagicMock(adapted_class_name='klasse')
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)
    result = ber._object_name

    assert result == 'klasse'


@patch(Patches.PostRequest)
@patch(Patches.PostInteractor)
def test_ber_instantiate_interactor(mock_inter, mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class)
    result = ber._instantiate_post_interactor(mock_req)

    mock_inter.assert_called_with(mock_req, mock_adapter, mock_class)
    assert result == mock_inter.return_value


@patch(Patches.PostRequest)
def test_ber_instantiate_custom_interactor(mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    mock_inter = MagicMock()
    ber = BasicEntityRoutes(mock_adapter, mock_class, mock_inter)
    result = ber._instantiate_post_interactor(mock_req)

    mock_inter.assert_called_with(mock_req, mock_adapter)
    assert result == mock_inter.return_value


@patch(Patches.DeleteRequest)
def test_ber_instantiate_custom_delete_interactor(mock_req):
    mock_adapter = MagicMock()
    mock_class = MagicMock()
    mock_inter = MagicMock()
    ber = BasicEntityRoutes(adapter_instance=mock_adapter,
                            entity_class=mock_class,
                            custom_delete_interactor_calss=mock_inter)
    result = ber._instantiate_delete_interactor(mock_req)

    mock_inter.assert_called_with(mock_req, mock_adapter)
    assert result == mock_inter.return_value
