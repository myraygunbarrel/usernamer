from marshmallow import Schema, fields
from usernamer.schemas.user import CommonUserFields


class ReporterQuery(Schema):
    added_from = fields.Date(required=True)
    added_to = fields.Date(required=True)


class UserReporterSchema(CommonUserFields):
    first_name = fields.Str()
    last_name = fields.Str()
    id = fields.Int()
    created_at = fields.Date()
    updated_at = fields.Date()
