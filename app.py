from flask import Flask, request, abort, jsonify, render_template, redirect, \
    url_for
from flask_migrate import Migrate
from database.models import setup_db, db, db_drop_and_create_all, Volunteer
from utils.phoneutils import *

app = Flask(__name__)
setup_db(app)
migrate = Migrate(app, db, compare_type=True)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('get_volunteers'))


@app.route('/volunteers', methods=['GET'])
def get_volunteers():
    volunteers = Volunteer.query.all()
    volunteers = [volunteer.format() for volunteer in volunteers]
    return render_template('volunteers.html', volunteers=volunteers)

    # return jsonify({
    #     'success': True,
    #     'volunteers': [v.format() for v in volunteers]
    # })


@app.route('/volunteers', methods=['POST'])
def post_volunteer():
    if request.data == b'':
        abort(400)
    body = request.get_json()
    if 'name' not in body or 'phone' not in body or 'email' not in body:
        abort(400)

    try:
        phone = get_phone_save_format(body['phone'])
        volunteer = Volunteer(name=body['name'], phone=phone, email=body['email'])
        volunteer.insert()
        db.session.commit()
        return jsonify({
            'success': True,
            'volunteer': volunteer.format()
        })
    except Exception as e:
        db.session.rollback()
        print(e)
        abort(422)


@app.route('/volunteers/<int:volunteer_id>', methods=['DELETE'])
def delete_volunteer(volunteer_id):
    volunteer = Volunteer.query.filter_by(id=volunteer_id).one_or_none()
    if not volunteer:
        abort(404)

    try:
        volunteer.delete()
        db.session.commit()
        return jsonify({
            'success': True,
            'volunteer': volunteer.format()
        })
    except Exception as e:
        db.session.rollback()
        print(e)
        abort(422)


@app.errorhandler(400)
def bad_request(ex):
    return jsonify({
        'success': False,
        'status_code': 400,
        'message': 'Bad request'
    }), 400


@app.errorhandler(404)
def not_found(ex):
    return jsonify({
        'success': False,
        'status_code': 404,
        'message': 'Not found'
    }), 404


@app.errorhandler(422)
def unprocessable(ex):
    return jsonify({
        'success': False,
        'status_code': 422,
        'message': 'Unprocessable'
    }), 422


if __name__ == '__main__':
    app.run(debug=True)
