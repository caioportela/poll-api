from flask import Blueprint, abort, jsonify, request

from api.database import get_db
from api.models.poll import Poll, PollSchema
from api.models.poll_option import PollOption, PollOptionSchema

bp = Blueprint('poll', __name__)

@bp.route('/poll/<poll_id>', methods=['GET'])
def poll_info(poll_id):
    """Return info about the given poll."""

    db_session = get_db()
    poll_schema = PollSchema()

    poll = Poll.query.get(poll_id)

    # Check if poll was found
    if poll is None:
        abort(404, description='Poll was not found')

    # Add the number of views
    poll.views += 1
    db_session.commit()

    # Serialize Poll
    poll = poll_schema.dump(poll)

    return jsonify(poll)

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

@bp.route('/poll/<poll_id>/stats', methods=['GET'])
def poll_stats(poll_id):
    """Return stats of the poll."""

    poll = Poll.query.get(poll_id)

    # Check if poll was found
    if poll is None:
        abort(404, description='Poll was not found')

    # Map stats
    stats = {
        'views': poll.views,
        'votes': [{'option_id': option.id, 'qty': option.votes} for option in poll.options]
    }

    return jsonify(stats)
    
@bp.route('/poll/<option_id>/vote', methods=['POST'])
def compute_vote(option_id):
    """Compute a vote for the given option."""

    db_session = get_db()

    option = PollOption.query.get(option_id)

    # Check if option exists
    if option is None:
        abort(404, description='Poll option was not found')

    # Add a vote for the option
    option.votes += 1
    db_session.commit()

    return jsonify({'option_id':option.id})
