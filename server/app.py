from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# api = Api(app)

# to prevent Proxy error: Could not proxy request /activities from localhost:4000 to http://localhost:5555.
# in package.json change "proxy": "http://localhost:5555", to 127.0.0.1:5555

@app.route('/')
def index():
    response = make_response(
        {
            "message": "Hello Campers!"
        },
        200
    )
    return response

# GET, POST /campers
@app.route('/campers', methods=['GET', 'POST'])
def camper():
    campers = Camper.query.all()
    if request.method == 'GET':
        return make_response([camper.to_dict() for camper in campers], 200)
        # campers_list = [] 
        # for camper in campers:
        #     campers_list.append(camper.to_dict())
        # response = make_response(campers_list, 200)
    elif request.method == 'POST':
        try:
            new_camper = Camper(
                name=request.get_json()['name'],
                age=request.get_json()['age']
            )
            db.session.add(new_camper)
            db.session.commit()

            return make_response(new_camper.to_dict(), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400 )

# GET /campers/:id
@app.route('/campers/<int:id>', methods=['GET'])
def camper_by_id(id):
    camper = Camper.query.filter_by(id=id).first()
    if camper:
        return make_response(camper.to_dict(), 200)
    return make_response({"error": "Camper not found"}, 404)

# GET /activities
@app.route('/activities', methods=['GET'])
def activity():
    activities = Activity.query.all()
    return make_response([activity.to_dict() for activity in activities], 200)

# DELETE /activities/:id
@app.route('/activities/<int:id>', methods=['DELETE'])
def activity_by_id(id):
    activity = Activity.query.filter_by(id=id).first()
    if activity:
        db.session.delete(activity)
        db.session.commit()
        return make_response('', 200)
    return make_response({"error": "Activity not found"}, 404)

# POST /signups
@app.route('/signups', methods=['POST'])
def signup():
    try:
        new_signup = Signup(
            time=request.get_json()['time'],
            camper_id=request.get_json()['camper_id'],                                                         
            activity_id=request.get_json()['activity_id']                                                         
        )
        db.session.add(new_signup)
        db.session.commit()

        return make_response(new_signup.to_dict(), 201)
    except ValueError:
        return make_response({"errors": ["validation errors"]}, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
