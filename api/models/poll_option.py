from sqlalchemy import Column, ForeignKey, Integer, String
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from api.database import Base

class PollOption(Base):
    __tablename__ = 'poll_option'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    votes = Column(Integer, default=0)

    poll_id = Column(Integer, ForeignKey('poll.id'))

class PollOptionSchema(SQLAlchemySchema):
    class Meta:
        model = PollOption
        load_instance = True

    option_id = auto_field('id')
    option_description = auto_field('description')
