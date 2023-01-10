from marshmallow import (
    Schema,
    fields,
    pre_dump,
)


class SanicQuerySchema(Schema):
    @pre_dump
    def query_list_to_normal_values(self, data, many, **kwargs):
        """Sanic Request feature"""
        for key, value in data.items():
            data[key] = value[0]
        return data


class IncrementSuspicionSchema(Schema):
    id = fields.String(required=True)
    suspicion = fields.Int(required=True)


class IncrementSuspicionBody:
    id = str
    suspicion = int


class GetSuspicionSchema(SanicQuerySchema):
    id = fields.String(required=True)
