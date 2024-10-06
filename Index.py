import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Database connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='*********',
            password='*********',
            database='********'
        )
        if conn.is_connected():
            print("Successfully connected to the database")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
def Index():
    return render_template('Index.html')

@app.route('/about')
def About():
    return render_template('About.html')

@app.route('/fleet')
def Fleet():
    conn = get_db_connection()
    vehicles = []

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT model_name, image, price_per_day, fuel_capacity FROM vehicles")
        vehicles = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('Fleet.html', vehicles=vehicles)

@app.route('/contact', methods=['GET', 'POST'])
def Contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO contact (name, email, subject, message) VALUES (%s, %s, %s, %s)',
                (name, email, subject, message)
            )
            conn.commit()
            cursor.close()
            conn.close()

        return redirect(url_for('Contact'))
    return render_template('Contact.html')

@app.route('/booknow', methods=['GET', 'POST'])
def Booknow():
    if request.method == 'POST':
        car = request.form['car']
        pickup_date = request.form['pickup_date']
        pickup_time = request.form['pickup_time']
        dropoff_date = request.form['dropoff_date']
        dropoff_time = request.form['dropoff_time']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        additional_services = request.form['additional_services']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO booking (car, pickup_date, pickup_time, dropoff_date, dropoff_time, name, email, phone, address, additional_services) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (car, pickup_date, pickup_time, dropoff_date, dropoff_time, name, email, phone, address, additional_services)
            )
            conn.commit()
            cursor.close()
            conn.close()

        return redirect(url_for('Booknow'))
    return render_template('Booknow.html')

@app.route('/book/<int:car_id>', methods=['POST'])
def book_car(car_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE vehicles SET status = 'Booked' WHERE id = %s", (car_id,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('Fleet'))

@app.route('/privacy-policy')
def Policy():
    return render_template('Policy.html')

@app.route('/terms-of-service')
def Ts():
    return render_template('Ts.html')

if __name__ == '__main__':
    app.run(debug=True)
