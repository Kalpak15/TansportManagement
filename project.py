from flask import *
from flask_sqlalchemy import SQLAlchemy
import MySQLdb
from datetime import datetime
"kalpak"
app=Flask(__name__)
app.secret_key="xac"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/college'
app.config['SQLALCHEMY_MODIFICATIONS']=True

db = SQLAlchemy(app)
class Signup(db.Model):
   sno= db.Column(db.Integer, primary_key = True,unique=True,nullable=False)
   name = db.Column(db.String(50),unique=False,nullable=False)
   email = db.Column(db.String(50),unique=True,nullable=False)
   address = db.Column(db.String(100),unique=False,nullable=False)
   password = db.Column(db.String(50),unique=False,nullable=False)
   confirm_password = db.Column(db.String(50),unique=False,nullable=False)

class Contact(db.Model):
   sno= db.Column(db.Integer, primary_key = True,unique=True,nullable=False)
   name = db.Column(db.String(50),unique=False,nullable=False)
   email = db.Column(db.String(50),unique=True,nullable=False)
   phone_num = db.Column(db.String(50),unique=False,nullable=False)
   mes = db.Column(db.String(50), unique=False, nullable=False)

class Calendar(db.Model):
    sno = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    from_date = db.Column(db.String(50), unique=False, nullable=False)
    to_date = db.Column(db.String(50), unique=False, nullable=False)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    speed = db.Column(db.Integer, unique=False, nullable=False)
    seats = db.Column(db.Integer, unique=False, nullable=False)
    image_url = db.Column(db.String(100), unique=False, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_email = db.Column(db.String(50), db.ForeignKey('signup.email'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=True)  # Make it nullable
    booking_date = db.Column(db.String(50), nullable=False)
    from_date = db.Column(db.String(50), nullable=False)  # New field for from_date
    to_date = db.Column(db.String(50), nullable=False)  # New field for to_date


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    price_per_day = db.Column(db.Integer, unique=False, nullable=False)
    image_url = db.Column(db.String(100), unique=False, nullable=False)

class DriverBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_email = db.Column(db.String(50), db.ForeignKey('signup.email'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    booking_date = db.Column(db.String(50), nullable=False)
    from_date = db.Column(db.String(50), nullable=False)  # New field for from_date
    to_date = db.Column(db.String(50), nullable=False)  # New field for to_date




@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method=="POST":
        Username = request.form['name']
        Email = request.form['email']
        Phone=request.form['phone']
        Message=request.form['message']

        entry = Contact(name=Username, email=Email,phone_num=Phone,mes=Message)
        db.session.add(entry)
        db.session.commit()

    return render_template("contact.html")



@app.route("/bookings")
def bookings():
    if 'email' in session:
        return render_template('bookings.html')
    else:
        return render_template("signup.html")


# //corrected 1
# @app.route('/book_car', methods=['POST'])
# def book_car():
#     if 'email' in session:
#         car_id = request.form['car_id']  # Get the car ID from the form
#         user_email = session['email']  # Get the email of the logged-in user
#
#         # Check if the car is already booked by any user
#         existing_booking = Booking.query.filter_by(car_id=car_id).first()
#
#         if existing_booking:
#             # If the car is already booked, show an error message
#             message = "This car is already booked by another user!"
#             return render_template('cars.html', cars=Car.query.all(), message=message)
#         else:
#             # If the car is not booked, proceed with the booking
#             booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             new_booking = Booking(user_email=user_email, car_id=car_id, booking_date=booking_date)
#             db.session.add(new_booking)
#             db.session.commit()
#
#             # Redirect to the calendar page after a successful booking
#             return redirect(url_for('calender'))
#     else:
#         return redirect(url_for('login'))  # Redirect to login if the user is not logged in

#
@app.route('/book_car', methods=['POST'])
def book_car():
    if 'email' in session:
        car_id = request.form['car_id']  # Get the car ID from the form
        user_email = session['email']  # Get the email of the logged-in user

        # Check if the car is already booked by any user
        existing_booking = Booking.query.filter_by(car_id=car_id).first()

        if existing_booking:
            # If the car is already booked, show an error message
            # message = "This car is already booked by another user!"
            return render_template('already.html')
            car_list = Car.query.all()  # Fetch all cars again
            return render_template('cars.html', cars=car_list, message=message)
        else:
            # Render the calendar page with car_id passed in
            return render_template('calender.html', car_id=car_id)  # Pass the car ID to calendar page
    else:
        return redirect(url_for('login'))

#
# @app.route('/cancel_booking', methods=['POST'])
# def cancel_booking():
#     if 'email' in session:
#         user_email = session['email']  # Get the user's email
#         car_id = request.form['car_id']  # Get the car ID from the form
#
#         # Find the booking to delete
#         booking_to_delete = Booking.query.filter_by(user_email=user_email, car_id=car_id).first()
#
#         if booking_to_delete:
#             db.session.delete(booking_to_delete)
#             db.session.commit()
#             message = "Your booking has been successfully canceled."
#         else:
#             message = "No booking found for this car."
#
#         # Render cars.html again with the message
#         return render_template('cars.html', cars=Car.query.all(), message=message)
#     else:
#         return redirect(url_for('login'))  # Redirect to login if the user is not logged in

@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    if 'email' in session:
        user_email = session['email']  # Get the user's email from the session
        car_id = request.form['car_id']  # Get the car ID from the form


        # Debugging: Print or log the user_email and car_id
        print(f"User email: {user_email}, Car ID: {car_id}")

        # Find the booking to delete
        booking_to_delete = Booking.query.filter_by(user_email=user_email, car_id=car_id).first()


        if booking_to_delete:
            try:
                db.session.delete(booking_to_delete)  # Delete the booking
                db.session.commit()  # Commit the changes to the database
                message = "Your booking has been successfully canceled."
                print("Booking canceled successfully.")
            except Exception as e:
                db.session.rollback()  # Rollback if there's an error
                message = "An error occurred while canceling your booking. Please try again."
                print(f"Error while canceling booking: {e}")
        else:
            message = "No booking found for this car."
            print("No booking found for the specified car.")

        # You can pass the message to the frontend
        return render_template('some_template.html', message=message)
    else:
        return redirect(url_for('login'))  # If the user is not logged in, redirect to the login page



# correct-1
# @app.route('/confirm_booking', methods=['POST'])
# def confirm_booking():
#     if 'email' in session:
#         user_email = session['email']
#         car_id = request.form['car_id']
#         from_date = request.form['from_date']
#         to_date = request.form['to_date']
#
#         # Get the current date and time for booking_date
#         booking_date = datetime.now()  # Current date and time
#
#         # Create a new booking entry
#         new_booking = Booking(user_email=user_email, car_id=car_id, booking_date=booking_date, from_date=from_date,
#                               to_date=to_date)
#
#         try:
#             db.session.add(new_booking)
#             db.session.commit()
#             flash("Booking confirmed successfully!")  # Flash message for success
#         except Exception as e:
#             db.session.rollback()  # Roll back the session on error
#             flash("An error occurred while confirming the booking: " + str(e))  # Flash error message
#
#         return redirect(url_for('home'))  # Redirect to some view after booking
#     else:
#         return redirect(url_for('login'))  # Redirect to login if the user is not logged in

# corrcetd at peak
@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    if 'email' in session:
        user_email = session['email']
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        car_id = request.form['car_id']  # Get the car_id from the form
        driver_id = request.form.get('driver_id')  # Get the driver_id if present

        # Check for overlapping bookings for the car
        existing_booking = Booking.query.filter(
            Booking.car_id == car_id,
            (Booking.from_date <= to_date) & (Booking.to_date >= from_date)
        ).first()

        if existing_booking:
            message = "The selected dates overlap with an existing booking."
            return render_template('calender.html', message=message, car_id=car_id)

        # Save the new booking
        new_booking = Booking(
            user_email=user_email,
            car_id=car_id,
            driver_id=driver_id,  # Include driver_id in the booking
            booking_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            from_date=from_date,
            to_date=to_date
        )
        db.session.add(new_booking)
        db.session.commit()

        message = "Your booking has been successfully done from {} to {}.".format(from_date, to_date)
        return render_template('calender.html', message=message)
    else:
        return redirect(url_for('login'))




@app.route('/cars')
def cars():
    car_list = [
        {
            'id': 1,
            'name': 'Maruti Suzuki',
            'price': 20000,
            'speed': 150,
            'seats':7,
            'image_url': 'assets/img/Maruti_Suzuki.jpeg'
        },
        {
            'id': 2,
            'name': 'Toyota XUV',
            'price': 22000,
            'speed': 160,
            'seats': 6,
            'image_url': 'assets/img/Toyota_XUV.jpeg'
        },
        {
            'id': 3,
            'name': 'Tata Altroz',
            'price': 18000,
            'speed': 140,
            'seats': 6,
            'image_url': 'assets/img/Tata_Altroz.jpeg'
        },
        {
            'id': 4,
            'name': 'Mahindra XUV',
            'price': 25000,
            'speed': 170,
            'seats': 5,
            'image_url': 'assets/img/Mahindra_XUV.jpg'
        },
        {
            'id': 5,
            'name': 'Mahindra Thar',
            'price': 30000,
            'speed': 165,
            'seats': 4,
            'image_url': 'assets/img/mahindra_thar.jpg'
        }
    ]
    return render_template('cars.html', cars=car_list)

# drivers = [
#     {"id": 1, "name": "Kalpak", "price_per_day": 1500, "image": "Driver.png"},
#     {"id": 2, "name": "Tejas", "price_per_day": 1000, "image": "Driver.png"},
#     {"id": 3, "name": "Rohan", "price_per_day": 1100, "image": "Driver.png"},
#     {"id": 4, "name": "Ramesh", "price_per_day": 1200, "image": "Driver.png"},
#     {"id": 5, "name": "Arpit", "price_per_day": 1300, "image": "Driver.png"},
#     {"id": 6, "name": "Abhijit", "price_per_day": 1400, "image": "Driver.png"},
# ]

@app.route('/drivers')
def drivers():
    drivers = [
        {"id": 1, "name": "Kalpak", "price_per_day": 1500, "image": "Driver.png"},
        {"id": 2, "name": "Tejas", "price_per_day": 1000, "image": "Driver.png"},
        {"id": 3, "name": "Rohan", "price_per_day": 1100, "image": "Driver.png"},
        {"id": 4, "name": "Ramesh", "price_per_day": 1200, "image": "Driver.png"},
        {"id": 5, "name": "Arpit", "price_per_day": 1300, "image": "Driver.png"},
        {"id": 6, "name": "Abhijit", "price_per_day": 1400, "image": "Driver.png"},
    ]
    message = "Select a driver to book"
    return render_template('drivers.html', drivers=drivers, message=message)

@app.route('/book_driver', methods=['POST'])
def book_driver():
    if 'email' in session:
        driver_id = request.form['driver_id']  # Get the driver ID from the form
        user_email = session['email']  # Get the email of the logged-in user

        # Check if the driver is already booked by any user
        existing_booking = DriverBooking.query.filter_by(driver_id=driver_id).first()

        if existing_booking:
            # If the driver is already booked, show an error message
            message = "This driver is already booked by another user!"
            return render_template('drivers.html', drivers=Driver.query.all(), message=message)
        else:
            # Render the calendar page with driver_id passed in
            return render_template('calender.html', driver_id=driver_id)  # Pass the driver ID to calendar page
    else:
        return redirect(url_for('login'))
#
# # //aall perfect is your code
# @app.route('/confirm_driver_booking', methods=['POST'])
# def confirm_driver_booking():
#     if 'email' in session:
#         user_email = session['email']
#         from_date_str = request.form['from_date']
#         to_date_str = request.form['to_date']
#         driver_id = int(request.form.get('driver_id', 0))
#
#         # Convert strings to datetime objects
#         from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
#         to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
#
#         # Check for overlapping bookings for the driver
#         existing_booking = DriverBooking.query.filter(
#             DriverBooking.driver_id == driver_id,
#             (DriverBooking.from_date <= to_date) & (DriverBooking.to_date >= from_date)
#         ).first()
#
#         if existing_booking:
#             message = "The selected dates overlap with an existing booking for this driver."
#             return render_template('calender.html', message=message, driver_id=driver_id)
#
#         # Save the new driver booking
#         new_driver_booking = DriverBooking(
#             user_email=user_email,
#             driver_id=driver_id,  # Ensure this is set correctly
#             booking_date=datetime.now(),
#             from_date=from_date,
#             to_date=to_date
#         )
#
#         try:
#             db.session.add(new_driver_booking)
#             db.session.commit()
#             message = "Your driver booking has been successfully made."
#         except Exception as e:
#             db.session.rollback()
#             message = f"An error occurred while booking: {str(e)}"
#
#         return render_template('calender.html', message=message)
#     else:
#         return redirect(url_for('login'))




@app.route('/confirm_driver_booking', methods=['POST'])
def confirm_driver_booking():
    if 'email' in session:
        user_email = session['email']
        from_date_str = request.form['from_date']
        to_date_str = request.form['to_date']
        driver_id = int(request.form.get('driver_id', 0))

        # Convert strings to datetime objects
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')

        # Check for overlapping bookings for the driver
        existing_booking = DriverBooking.query.filter(
            DriverBooking.driver_id == driver_id,
            DriverBooking.from_date <= to_date,  # Overlapping condition
            DriverBooking.to_date >= from_date
        ).first()

        if existing_booking:
            # If the driver is already booked for the selected dates, show an error message
            message = "The selected dates overlap with an existing booking for this driver."
            return render_template('calender.html', message=message, driver_id=driver_id)

        # If no overlapping booking, proceed with the new driver booking
        new_driver_booking = DriverBooking(
            user_email=user_email,
            driver_id=driver_id,
            from_date=from_date,
            to_date=to_date,
            booking_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        db.session.add(new_driver_booking)
        db.session.commit()

        message = f"Driver booked successfully from {from_date_str} to {to_date_str}."
        return render_template('calender.html', message=message)
    else:
        return redirect(url_for('login'))


@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        Username = request.form['username']
        Email = request.form['email']
        Address = request.form['address']
        Password = request.form['password']
        Confirm_password = request.form['confirm_password']

        if Password == Confirm_password:
            entry = Signup(name=Username, email=Email, address=Address, password=Password, confirm_password=Confirm_password)
            db.session.add(entry)
            db.session.commit()
            return redirect('/login')
        else:
            msg = "Passwords do not match"
            return render_template("signup.html", msg=msg)

    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    # if 'user' in session:
    #     message = "You are already logged in"
    #     return render_template('index.html')
    if request.method == 'POST':
        Email = request.form['email']
        Password = request.form['password']
        user = Signup.query.filter_by(email=Email).first()

        if user and user.password == Password:
            session['email'] =Email
            message = "You have successfully logged in"
            return render_template('index.html',msg=message)
        else:
            msg = "Invalid username or password"
            return render_template("login.html", msg=msg)

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('email',None)
    return  redirect('/')

# @app.route('/drivers')
# def drivers():
#     return render_template('drivers.html')



@app.route("/calender")
def calender():
    return render_template("calender.html")



if __name__=='__main__':
    app.run(debug=True)
