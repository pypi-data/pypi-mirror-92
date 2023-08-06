from functools import reduce
from typing import List

from clean_architecture_basic_classes import BasicEntity


class RangedList:
    def __init__(self, object_list, initial, final, total, unit):
        self.object_list = object_list
        self.initial = initial
        self.final = final
        self.total = total
        self.unit = unit


class BasicGetAllRequestModel:
    def __init__(self, query_params, unit='itens'):
        params = query_params if query_params else {}

        self.pagination_page = int(params.get('pagination_page', 1))
        self.pagination_per_page = int(params.get('pagination_perPage', 10))
        self.sort_field = params.get('sort_field')
        self.sort_order = params.get('sort_order')
        self.filter_field = params.get('filter_field')
        self.filter_value = params.get('filter_value')
        self.unit = unit


class BasicGetAllResponseModel:
    def __init__(self,
                 entities: List[BasicEntity],
                 initial, final, total, unit):
        self.entities: List[BasicEntity] = entities
        self.initial = initial
        self.final = final
        self.total = total
        self.unit = unit

    def __call__(self):
        entities = [x.to_json() for x in self.entities]

        return RangedList(entities,
                          self.initial,
                          self.final,
                          self.total,
                          self.unit)


class BasicGetAllInteractor:
    def __init__(self,
                 request: BasicGetAllRequestModel,
                 adapter_instance):
        self.adapter_instance = adapter_instance
        self.request: BasicGetAllRequestModel = request

    @staticmethod
    def item_range_by_page(per_page, page):
        inicio = (page - 1) * per_page
        fim = inicio + per_page

        return inicio, fim

    def run(self):
        result = self._list_items()

        ordenado = self._get_sorted_items(result)

        fim, inicio, paginado = self._get_paginated_items(ordenado)

        response = BasicGetAllResponseModel(paginado,
                                            inicio,
                                            fim-1,
                                            len(result),
                                            self.request.unit)
        return response()

    def _get_paginated_items(self, ordenado):
        inicio, fim = self.item_range_by_page(self.request.pagination_per_page,
                                              self.request.pagination_page)
        paginado = ordenado[inicio:fim]
        return fim, inicio, paginado

    def _get_sorted_items(self, result):
        if self.request.sort_field:
            ordenado = self._sort_items(result)
        else:
            ordenado = self._unsorted_items(result)
        return ordenado

    def _unsorted_items(self, result):
        ordenado = result
        return ordenado

    def _sort_items(self, result):
        ordenado = sorted(
            result,
            key=lambda x: self._get_sort_key(x),
            reverse=self.request.sort_order == 'DESC')
        return ordenado

    def _get_sort_key(self, x):
        fields = self.request.sort_field.split('_dot_')
        return reduce(getattr, fields, x)

    def _list_items(self):
        filtered = (bool(self.request.filter_field) and
                    bool(self.request.filter_value))
        fn_map = {True: self._list_filtered, False: self._list_unfiltered}
        fn_list = fn_map[filtered]
        result = fn_list()
        return result

    def _list_unfiltered(self):
        result = self.adapter_instance.list_all()
        return result

    def _list_filtered(self):
        arg_key = f'{self.request.filter_field}__contains'
        result = self.adapter_instance.filter(
            **{arg_key: self.request.filter_value})
        return result
