from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from api.database import Base
from api.models.poll_option import PollOption, PollOptionSchema

class Poll(Base):
    __tablename__ = 'poll'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    views = Column(Integer, default=0)

    options = relationship(PollOption, backref='poll', lazy=True)

class PollSchema(SQLAlchemySchema):
    class Meta:
        model = Poll
        load_instance = True

    poll_id = auto_field('id')
    poll_description = auto_field('description')
    options = Nested(PollOptionSchema, many=True)
