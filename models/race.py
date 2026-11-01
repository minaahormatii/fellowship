import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db


class Races(db.Model):
    __tablename__ = "Races"

    race_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    race_name = db.Column(db.String(), nullable=False, unique=True)
    homeland = db.Column(db.String())
    lifespan = db.Column(db.Integer())

    heros = db.relationship(
        "Heros",
        back_populates="races",
        cascade="all, delete-orphan", 
    )

    def __init__(self, race_name, homeland=None, lifespan=None):
        self.race_name = race_name
        self.homeland = homeland
        self.lifespan = lifespan

    def new_race_obj():
            return Races("", "", 0)


class RacesSchema(ma.Schema):
    class Meta:
        fields = ['race_id', 'race_name', 'homeland', 'lifespan', 'heros']

    race_id = ma.fields.UUID()
    race_name = ma.fields.String(required=True)
    homeland = ma.fields.String(allow_none=True)
    lifespan = ma.fields.Integer(allow_none=True)
    heros = ma.fields.Nested("HerosSchema", many=True, exclude=['race'])


race_schema = RacesSchema()
races_schema = RacesSchema(many=True)