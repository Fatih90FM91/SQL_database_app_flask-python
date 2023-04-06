import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

api_key_allowed = 'TopSecretAPIKey'
app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}


            # Loop through each column in the data record
        for column in self.__table__.columns:

            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record

@app.route("/random")
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)

    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all_cafes", methods=['GET'])
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    all_cafe = [items.to_dict() for items in cafes]
    print(all_cafe)

    return jsonify(cafe=all_cafe)


@app.route("/search/<location>", methods=['GET'])
def get_cafe_search(location):
    try:
        cafe = Cafe.query.filter_by(location=location).first()
        # all_cafe = [items.to_dict() for items in cafe]
        print(cafe)


        return jsonify(cafe=cafe.to_dict())

    except AttributeError:

        dictionary = {
            'error': {
                'Not Found': 'Sorry, we dont have a cafe at that location.'
            }
        }

        return jsonify(cafe=dictionary)
    #Simply convert the random_cafe data record to a dictionary of key-value pairs.


## HTTP POST - Create Record

@app.route("/add", methods=['POST'])
def add_cafes():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )

    db.session.add(new_cafe)
    db.session.commit()

    #Simply convert the random_cafe data record to a dictionary of key-value pairs.
    return jsonify(response={'success':'Successfully added the new cafe.'})


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=['GET', 'POST', 'PATCH'])
def update_cafe_price(cafe_id):
    try:
        cafe_price_to_update = Cafe.query.get(cafe_id)
        print(cafe_price_to_update)
        print(cafe_price_to_update.coffee_price)
        cafe_price_to_update.coffee_price = request.form.get("new_price")
        print(cafe_price_to_update.coffee_price)
        db.session.commit()


        #Simply convert the random_cafe data record to a dictionary of key-value pairs.
        return jsonify(response={'success':'Successfully added the new cafe.'})
    except AttributeError:

        dictionary = {
            'error': {
                'Not Found': 'Sorry, we dont have a cafe at that location.'
            }
        }

        return jsonify(cafe=dictionary)


## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['GET', 'DELETE'])
def delete_cafes(cafe_id):
    try:
        searchword = request.args.get('api-key')
        if searchword == api_key_allowed:
            cafe_delete = Cafe.query.get(cafe_id)
            db.session.delete(cafe_delete)
            db.session.commit()

            return jsonify(response={'success':'Successfully a cafe with that id was deleted.'})
        else:
            dictionary = {
                'error': {
                    'Not Allowed': 'Sorry, that is not allowed. Make sure you have the correct api-key.'
                }
            }

            return jsonify(cafe=dictionary)





    except AttributeError:

        dictionary = {
            'error': {
                'Not Found': 'Sorry, a cafe with that id was not found in DATABASE.'
            }
        }

        return jsonify(cafe=dictionary)


if __name__ == '__main__':
    app.run(debug=True)
