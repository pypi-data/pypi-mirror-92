from marshmallow import ValidationError

from clean_architecture_basic_classes.basic_interactors.basic_delete import (
    BasicDeleteInteractor,
    BasicDeleteRequestModel,
    BasicDeleteResponseModel
)
from clean_architecture_basic_classes.basic_interactors.basic_get import (
    BasicGetRequestModel,
    BasicGetInteractor,
    BasicGetResponseModel
)
from clean_architecture_basic_classes.basic_interactors.basic_get_all import (
    BasicGetAllInteractor,
    BasicGetAllRequestModel,
    BasicGetAllResponseModel)
from clean_architecture_basic_classes.basic_interactors.basic_post import (
    BasicPostRequestModel,
    BasicPostInteractor,
    SaveEntityException,
    BasicPostResponseModel
)
from clean_architecture_basic_classes.basic_interactors.basic_put import (
    BasicPutRequestModel,
    BasicPutInteractor,
    UpdateEntityException,
    BasicPutResponseModel
)
from clean_architecture_basic_classes.basic_persist_adapter import \
    BasicPersistAdapter
from clean_architecture_basic_classes.basic_routes.exceptions import (
    UnexpectedErrorException,
    PutException,
    ValidationErrorException,
    PostException,
    NotFoundException)


class BasicEntityRoutes:
    def __init__(self,
                 adapter_instance,
                 entity_class,
                 custom_post_interactor_class=None,
                 custom_delete_interactor_calss=None):
        self.adapter_instance: BasicPersistAdapter = adapter_instance
        self.entity_class = entity_class

        self.post_interactor_class = custom_post_interactor_class
        self.delete_interactor_class = custom_delete_interactor_calss

    @property
    def _object_name(self):
        return self.adapter_instance.adapted_class_name

    def _instantiate_post_interactor(self, request):
        if self.post_interactor_class is None:
            return BasicPostInteractor(request,
                                       self.adapter_instance,
                                       self.entity_class)
        else:
            return self.post_interactor_class(request, self.adapter_instance)

    def _instantiate_delete_interactor(self, request):
        if self.delete_interactor_class is None:
            return BasicDeleteInteractor(request, self.adapter_instance)
        else:
            return self.delete_interactor_class(request, self.adapter_instance)

    def get_all(self, query_params, unit) -> BasicGetAllResponseModel:
        """
        Raises: ValidationErrorException,
                UnexpectedErrorException
        """
        try:
            request = BasicGetAllRequestModel(query_params, unit)
            interactor = BasicGetAllInteractor(request, self.adapter_instance)
            response = interactor.run()

            return response

        except ValidationError as e:
            msg = f'Erro de validação obtendo lista ' \
                  f'de {self._object_name}: {e}'
            raise ValidationErrorException(msg)

        except BaseException as e:
            msg = f'Erro obtendo lista de {self._object_name}: ' \
                  f'{type(e)}({e})'
            raise UnexpectedErrorException(msg)

    def get_by_id(self, entity_id) -> BasicGetResponseModel:
        """
        Raises: ValidationErrorException,
                UnexpectedErrorException,
                NotFoundException
        """
        try:
            request = BasicGetRequestModel(entity_id)
            interactor = BasicGetInteractor(request, self.adapter_instance)
            response = interactor.run()
            if response:
                return response

        except ValidationError as e:
            msg = f'Erro de validação obtendo ' \
                  f'{self._object_name} {entity_id}: {e}'
            raise ValidationErrorException(msg)

        except BaseException as e:
            msg = f'Erro obtendo {self._object_name} {entity_id}: ' \
                  f'{type(e)}({e})'
            raise UnexpectedErrorException(msg)

        raise NotFoundException(
            f'{self._object_name} {entity_id} não encontrado')

    def post(self, json_data) -> BasicPostResponseModel:
        """
        Raises: PostException,
                ValidationErrorException,
                UnexpectedErrorException
        """
        try:
            request = BasicPostRequestModel(json_data)
            interactor = self._instantiate_post_interactor(request)
            response = interactor.run()

            return response

        except SaveEntityException as e:
            msg = f'Erro gravando {self._object_name}: {e}'
            raise PostException(msg)

        except ValidationError as e:
            msg = f'Erro de validação criando {self._object_name}: {e}'
            raise ValidationErrorException(msg)

        except BaseException as e:
            msg = f'Erro criando {self._object_name}: ' \
                  f'{type(e)}({e})'
            raise UnexpectedErrorException(msg)

    def put(self, entity_id, json_data) -> BasicPutResponseModel:
        """
        Raises: PutException,
                ValidationErrorException,
                UnexpectedErrorException
        """
        try:
            request = BasicPutRequestModel(entity_id, json_data)
            interactor = BasicPutInteractor(request,
                                            self.adapter_instance,
                                            self.entity_class)
            response = interactor.run()
            return response

        except UpdateEntityException as e:
            msg = f'Erro atualizando {self._object_name} {entity_id}: {e}'
            raise PutException(msg)

        except ValidationError as e:
            msg = f'Erro de validação atualizando ' \
                  f'{self._object_name} {entity_id}: {e}'
            raise ValidationErrorException(msg)
        except BaseException as e:
            msg = f'Erro atualizando {self._object_name} {entity_id}: ' \
                  f'{type(e)}({e})'
            raise UnexpectedErrorException(msg)

    def delete(self, entity_id) -> BasicDeleteResponseModel:
        """
        Raises: NotFoundException,
                UnexpectedErrorException
        """
        try:
            request = BasicDeleteRequestModel(entity_id)
            interactor = self._instantiate_delete_interactor(request)
            response = interactor.run()
            if response:
                return response

        except BaseException as e:
            msg = f'Erro removendo {self._object_name} {entity_id}: ' \
                  f'{type(e)}({e})'
            raise UnexpectedErrorException(msg)

        raise NotFoundException(f'{self._object_name} não encontrado para '
                                f'ser deletado')
