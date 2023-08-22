from flask import Flask, request, jsonify
from models import db, User
from datetime import datetime

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthday_app.db'
db.init_app(app)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    birthdate_str = data.get('birthdate')

    if not name or not birthdate_str:
        return jsonify({"error": "Missing data"}), 400

    try:
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        new_user = User(name=name, birthdate=birthdate)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/check_birthday', methods=['GET'])
def check_birthday():
    today = datetime.now().date()
    users = User.query.filter_by(birthdate=today).all()
    if users:
        user_names = [user.name for user in users]
        return jsonify({"message": f"Today is the birthday of: {', '.join(user_names)}"})
    else:
        return jsonify({"message": "No birthdays today"})

if __name__ == '__main__':
    app.run(debug=True)
