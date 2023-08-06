from abc import ABC, abstractmethod
import logging


class BasicPersistAdapter(ABC):
    def __init__(self, adapted_class, logger=None):
        """
        Adapter para persistencia de um entity
        :param adapted_class: Classe sendo adaptada
        """
        self._class = adapted_class
        self._logger = logger if logger else logging.getLogger()

    @property
    def logger(self):
        return self._logger

    @property
    def adapted_class(self):
        return self._class

    @property
    def adapted_class_name(self):
        return self._class.__name__

    @abstractmethod
    def list_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, item_id):
        raise NotImplementedError

    @abstractmethod
    def save(self, serialized_data):
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id):
        raise NotImplementedError

    @abstractmethod
    def filter(self, **kwargs):
        """
        Filtra objetos de acordo com o critério especificado.
        Para especificar o critérios, que por default são concatenados
        com o operador lógico *ou*, use o nome do campo junto com o operador
        desejado concatenado com um "__" (duplo sublinha).
        Exemplo: Para filtrar todos os objetos em que o campo email seja
        igual à "nome@dom.com", o filtro deverá ser chamado assim:
            result = adapter.filter(email__eq="nome@dom.com")

        :raises ValueError(Comparador inválido): se o comparador especificado
            não for um dos seguintes:
               [begins_with, between, contains, eq, exists, gt, gte, is_in, lt,
                lte, ne, not_exists]

        :return: Lista de objetos
        """
        raise NotImplementedError
