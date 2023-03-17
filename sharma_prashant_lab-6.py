from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# The `app.config` dictionary is used to configure various settings
# for the Flask app. Here, we specify the database URI and set the
# `SQLALCHEMY_TRACK_MODIFICATIONS` option to `False`, which tells
# SQLAlchemy not to track changes to database objects unless we
# explicitly tell it to do so.
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@db:5432/3038516340"
db = SQLAlchemy(app)


# Define Quote model, which will map to a 'quotes' table in the database
class Quote(db.Model):
    day = db.Column(db.String(80), primary_key=True)
    quote = db.Column(db.String(80))

    def to_dict(self):
        return {"day": self.day, "quote": self.quote}


@app.route("/quotes/<day>")
def get_quote(day):
    quote = Quote.query.filter_by(day=day).first()
    if quote:
        return jsonify(quote.to_dict())
    else:
        return jsonify({"error": "Quote not found."})


@app.route("/quotes", methods=["POST"])
def add_quote():
    data = request.get_json()
    new_quote = Quote(day=data["day"], quote=data["quote"])
    db.session.add(new_quote)  # Allows us to add/post new rows to the table
    try:
        db.session.commit()  # Ensures that the data is actually written to the table - ACID properties anyone?
        return jsonify(new_quote.to_dict())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Quote already exists"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
