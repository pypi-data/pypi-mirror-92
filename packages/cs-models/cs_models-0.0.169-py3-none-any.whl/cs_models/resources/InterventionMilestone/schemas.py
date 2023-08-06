from marshmallow import (
    Schema,
    fields,
    validate,
)


class InterventionMilestoneResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    intervention_condition_id = fields.Integer(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    milestone = fields.String(validate=not_blank, required=True)
    description = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()


class InterventionMilestonePatchSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
