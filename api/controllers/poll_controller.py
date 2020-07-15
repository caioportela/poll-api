from flask import Blueprint, abort, jsonify, request

from api.database import get_db
from api.models.poll import Poll, PollSchema
from api.models.poll_option import PollOption, PollOptionSchema

bp = Blueprint('poll', __name__)

@bp.route('/poll', methods=['POST'])
def post_poll():
    """Insert a Poll and its options."""

    db_session = get_db()

    data = request.get_json(force=True)

    # Check if description was sent
    if 'poll_description' not in data:
        abort(400, description='"poll_description" was not sent')

    # Check if options were sent
    if 'options' not in data:
        abort(400, description='The poll options were not sent')

    # Check if "options" property is an array
    if type(data['options']) is not list:
        abort(400, description='"options" must be an array')

    poll = Poll(description=data['poll_description'])

    for option in data['options']:
        PollOption(description=option, poll=poll)

    db_session.add(poll)
    db_session.commit()

    return (jsonify({"poll_id": poll.id}), 201)
