from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'super_secret_key_lucia'

app.config[
    "SQLALCHEMY_DATABASE_URI"] = "postgresql://uwj8p4v8zuoeyv3iqlxg:Kh3N5D3JtxcCyJeXuUeeZVNCROL6Jo@b1mxnbtfaytwhs4af34m-postgresql.services.clever-cloud.com:50013/b1mxnbtfaytwhs4af34m"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Rides(db.Model):
    rides_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_location = db.Column(db.String(100), nullable=False)
    to_location = db.Column(db.String(100), unique=True)
    date = db.Column(db.DateTime)
    notes = db.Column(db.Text(255))


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.String(255), nullable=False)


class User_route(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    route = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    return redirect(url_for('menu'))


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user
        user = Users.query.filter_by(username=username).first()
        print(user.user_id)
        if user and user.password == password:
            # Successful login
            return redirect(url_for('welcome', username=username))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)


@app.route('/logout')
def logout():
    logout_users()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        notes = request.form['notes']

        # Add the new user to the database
        user = Users(username=username, password=password, email=email, notes=notes)
        db.session.add(user)
        db.session.commit()

        flash("User registered successfully!", "success")  # Add this line

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/create_ad', methods=['GET', 'POST'])
def create_ad():
    if request.method == 'POST':
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        date = request.form['date']
        notes = request.form['notes']

        try:
            ride = Rides(from_location=from_location, to_location=to_location, date=date, notes=notes)
            db.session.add(ride)
            db.session.commit()
            return redirect('/success')
        except Exception as e:
            print(f"Error inserting data: {str(e)}")
            return "An error occurred while inserting data. Please try again."

    return render_template('create_ad.html')


@app.route('/success')
def success():
    return 'Inzerát bol úspešne vytvorený!'


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')

        try:
            rides = Rides.query.filter(Rides.from_location.ilike(f"%{from_location}%")).all()

            if rides:
                filtered_rides = [ride for ride in rides if ride.to_location.lower() == to_location.lower()]
            else:
                filtered_rides = []  # No rides found

            if not filtered_rides:
                return "No rides found."  # Display a message when no rides match the criteria

            return render_template("search.html", rides=filtered_rides)
        except Exception as e:
            return f"Error: {str(e)}"
    rides = Rides.query.all()
    return render_template("search.html", rides=rides)

@app.route('/register_trip', methods=['POST'])
def register_trip():

    try:
        # Parse the ride ID from the request data (usually sent as JSON)
        data = request.get_json()
        rides_id = data.get('rideId')

        relationship = User_route(user=2, route=rides_id)
        db.session.add(relationship)
        db.session.commit()
        return jsonify({'message': 'User registered for trip successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/about')
def about():
    about_info = {
        'project_name': 'Názov nášho projektu',
        'description': 'Stručný popis projektu.',
        'developers': [
            {'name': 'Lucia Mihalikova', 'role': 'Developer'},
        ]
    }
    return render_template('about.html', about_info=about_info)


if __name__ == '__main__':
    app.run(debug=True)
