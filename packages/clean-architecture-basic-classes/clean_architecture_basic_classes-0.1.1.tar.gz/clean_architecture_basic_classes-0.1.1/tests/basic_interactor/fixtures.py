from marshmallow import fields, post_load
from clean_architecture_basic_classes import BasicEntity
from uuid import uuid4


class FakeEntity(BasicEntity):
    def __init__(self, entity_id=None, nome=None, idade=None):
        super(FakeEntity, self).__init__(entity_id)
        self.nome = nome
        self.idade = idade

    class Schema(BasicEntity.Schema):
        nome = fields.String(required=True, allow_none=False)
        idade = fields.Integer(required=True, allow_none=False)

        @post_load
        def post_load(self, data, many, partial, **kwargs):
            return FakeEntity(**data)


class FakeAdapter:
    def __init__(self, fake_db):
        self.fake_db = fake_db

    def save(self, json_data):
        entity_id = json_data.get('entity_id', str(uuid4()))
        json_data.update({'entity_id': entity_id})
        self.fake_db[json_data['entity_id']] = json_data

    def list_all(self):
        objects = [FakeEntity.from_json(x) for x in self.fake_db.values()]
        for obj in objects:
            obj.set_adapter(self)
        return objects

    def get_by_id(self, item_id):
        response = self.fake_db.get(item_id)
        if response is not None:
            return FakeEntity.from_json(response)

    def delete(self, entity_id):
        del self.fake_db[entity_id]
        return entity_id


def make_context(adapter, qtd=3):
    populacao = [('wilson', 3),
                 ('yankee', 44),
                 ('xavier', 67),
                 ('gabriel', 32),
                 ('juliet', 33),
                 ('samantha', 38),
                 ('ulisses', 98),
                 ('mike', 72),
                 ('homero', 21),
                 ('alice', 5),
                 ('isis', 42),
                 ('charlie', 10),
                 ('daneel', 20000),
                 ('bob', 8),
                 ('kate', 23),
                 ('fabio', 16),
                 ('romeu', 18),
                 ('zacarias', 23),
                 ('einstein', 80),
                 ('oscar', 11),
                 ('paulo', 32),
                 ('lucas', 7),
                 ('vitoria', 34),
                 ('tatiana', 42),
                 ('nickolas', 27)]
    entidades = populacao[:qtd]

    for nome, idade in entidades:
        fentity = FakeEntity(str(uuid4()), nome, idade)
        fentity.set_adapter(adapter)
        fentity.save()

    return entidades
