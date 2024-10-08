from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/random')
def random():
    random_cafe = db.session.query(Cafe).order_by(func.random()).first()
    return jsonify(cafe=random_cafe.to_dict())


# HTTP POST - Create Record
@app.route('/all')
def all_cafes():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()

    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route('/search')
def search():
    query_location = request.args.get("loc")
    cafes = db.session.execute(
        db.select(Cafe).order_by(Cafe.name).where(Cafe.location == query_location)).scalars().all()

    if len(cafes) != 0:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.args.get("name") or request.form.get("name"),
        map_url=request.args.get("map_url") or request.form.get("map_url"),
        img_url=request.args.get("img_url") or request.form.get("img_url"),
        location=request.args.get("loc") or request.form.get("loc"),
        has_sockets=bool(request.args.get("sockets") or request.form.get("sockets")),
        has_toilet=bool(request.args.get("toilet") or request.form.get("toilet")),
        has_wifi=bool(request.args.get("wifi") or request.form.get("wifi")),
        can_take_calls=bool(request.args.get("calls") or request.form.get("calls")),
        seats=request.args.get("seats") or request.form.get("seats"),
        coffee_price=request.args.get("coffee_price") or request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>', methods=["GET", "PATCH"])
def update(cafe_id):
    price = request.args.get('new_price')
    cafe_to_update = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if cafe_to_update:
        cafe_to_update.coffee_price = price
        db.session.commit()
        return jsonify(response={'success': 'Successfully update the cafe coffee price'}), 200
    else:
        return jsonify(error={'error': 'Sorry, a cafe with that id was not found in the database'}), 404


# HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=["GET", "DELETE"])
def delete(cafe_id):
    api_key = request.args.get('api_key')
    if api_key == "TopSecretAPIKey":
        cafe_to_delete = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(response={'success': 'Successfully deleted the cafe.'}), 200
        else:
            return (jsonify(error={'error': {'Not found': 'Sorry, a cafe with that id was not found in the database'}}),
                    404)

    else:
        return jsonify(error={"error": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True, port=5003)
