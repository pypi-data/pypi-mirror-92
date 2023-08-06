import logging


class UpdateEntityException(BaseException):
    pass


class BasicPutRequestModel:
    def __init__(self, entity_id, json_data):
        self.json_data = json_data
        self.entity_id = entity_id


class BasicPutResponseModel:
    def __init__(self, saved_entity):
        self.saved_entity = saved_entity

    def __call__(self):
        return self.saved_entity.to_json()


class BasicPutInteractor:
    def __init__(self, request: BasicPutRequestModel,
                 adapter_instance,
                 entity_class):
        self.request = request
        self.adapter_instance = adapter_instance
        self.entity_class = entity_class
        self.logger = logging.getLogger(__name__)

    def _init_entity(self):
        """
        Função que deve ser sobreescrita por classe derivada caso
        a criação da entidade com os dados do post não seja trivial

        :return: Instância da entidade.
        """
        entity = self.entity_class.from_json(self.request.json_data)
        entity.entity_id = self.request.entity_id
        return entity

    def run(self):
        entity = self._init_entity()
        entity.set_adapter(self.adapter_instance)
        try:
            entity.save()
            return BasicPutResponseModel(entity)()
        except Exception as e:
            msg = 'Erro alterando entidade: {}'.format(e)
            self.logger.error(msg)
            raise UpdateEntityException(msg)
