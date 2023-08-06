from marshmallow import fields, post_load
from clean_architecture_basic_classes import BasicValue
from clean_architecture_basic_classes.basic_domain.util import \
    generic_serialize_roundtrip_test


def test_basic_value_serialize():
    class DummyValue(BasicValue):
        def __init__(self, texto, numero):
            self.texto = texto
            self.numero = numero

        class Schema(BasicValue.Schema):
            texto = fields.Str()
            numero = fields.Number()

            @post_load
            def on_load(self, data, many, partial):
                return DummyValue(**data)

    value = DummyValue('texto', 42)
    generic_serialize_roundtrip_test(DummyValue, value)
