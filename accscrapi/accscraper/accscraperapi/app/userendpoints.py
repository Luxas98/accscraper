from accscraper.accscrapercore import RequestStorage
from .models import User
from flask import Blueprint, g, request, jsonify
from . import db
blueprint = Blueprint('user-endpoints', __name__)


@blueprint.route('/user/<user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user(user_id):
    g.endpoint = user.__name__
    RequestStorage.init_task_storage(
        {
            'endpoint': 'user',
            'method': request.method
        }
    )
    if request.method == 'GET':
        return _user_get(request, user_id)

    if request.method == 'POST':
        return _user_post(request, user_id)

    if request.method == 'PUT':
        return _user_put(request)

    if request.method == 'DELETE':
        return _user_delete(request)


def _user_get(request, user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    response = {"id": user.id, "name": user.first_name} if user else {}
    return jsonify(response)


def _user_post(request, user_id):
    request_data = request.get_json()
    user = User(user_id, request_data['first_name'], request_data['last_name'], request_data['price'], request_data['size'], request_data['distance'])
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "success": True
    })

def _user_delete(request):
    pass


def _user_put(request):
    pass
