from marshmallow import Schema


class BasicValue:
    @classmethod
    def from_json(cls, dict_data):
        return cls.Schema().load(dict_data)

    def to_json(self):
        return self.Schema().dump(self)

    def __eq__(self, other):
        return all([getattr(self, attr) == getattr(other, attr)
                    for attr in self.Schema().fields.keys()])

    class Schema(Schema):
        pass
