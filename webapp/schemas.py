from webapp import ma
from webapp.models import Location, User, UploadedData, VisualisationData, WaterQualityData
from marshmallow import fields

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True  

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    # To maintain password security, do not send the password to the client
    password = fields.Str(load_only=True)

class UploadedDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UploadedData
        load_instance = True

    user = fields.Nested(UserSchema(only=("user_id", "email")))
    location = fields.Nested(LocationSchema)

class VisualisationDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VisualisationData
        load_instance = True

    upload = fields.Nested(UploadedDataSchema)
    location = fields.Nested(LocationSchema)

class WaterQualityDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WaterQualityData
        load_instance = True

    # Include location details in water quality data
    location = fields.Nested(LocationSchema)


class WaterQualityUpdateDataSchema(ma.Schema):
    spec_cond_max = fields.Float(allow_none=True)
    ph_max = fields.Float(allow_none=True)
    ph_min = fields.Float(allow_none=True)
    spec_cond_min = fields.Float(allow_none=True)
    spec_cond_mean = fields.Float(allow_none=True)
    dissolved_oxy_max = fields.Float(allow_none=True)
    dissolved_oxy_mean = fields.Float(allow_none=True)
    dissolved_oxy_min = fields.Float(allow_none=True)
    temp_mean = fields.Float(allow_none=True)
    temp_min = fields.Float(allow_none=True)
    temp_max = fields.Float(allow_none=True)
    water_quality = fields.Float(allow_none=True)
    training = fields.Boolean(allow_none=True)