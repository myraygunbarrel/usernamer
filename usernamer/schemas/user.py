from marshmallow import Schema, fields


class UserGetPath(Schema):
    user_id = fields.Int(required=True)


class UserUpdateBody(Schema):
    id = fields.Int(required=True)
    date_fact = fields.Bool(required=True)
    year_fact = fields.Bool(required=True)


class UserBody(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    date_of_birth = fields.Date(required=True)


class CommonUserFields(Schema):
    date_of_birth = fields.Str()
    date_fact = fields.Str()
    year_fact = fields.Str()


class UserSchema(CommonUserFields):
    name = fields.Method("format_name", dump_only=True)

    def format_name(self, user):
        return "{} {}".format(user.first_name, user.last_name)

