"""
This contains the schema for posting questions
"""
from marshmallow import Schema, fields
from ..utils.validations import Not_null_string


class QuestionSchema(Schema):
    """ Class to validate schema for Question object """

    title = fields.Str(required=True, validate=Not_null_string)
    body = fields.Str(required=True, validate=Not_null_string)
