from flask import Flask, request, render_template  # Import necessary modules from Flask
from flaskext.mysql import MySQL  # Import the MySQL extension for Flask
import os

app = Flask(__name__)  # Create a Flask application instance
mysql = MySQL()  # Create an instance of the MySQL object

mysql.init_app(app)  # Initialize the MySQL extension with the Flask application
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_DATABASE_USER'] = os.environ.get('MYSQL_ROOT_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_ROOT_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('MYSQL_DB')


@app.route('/test_db')
def test_db():
    try:
        conn = mysql.connect()
        return 'Database connection successful'
    except Exception as e:
        return 'Database connection failed: ' + str(e)

@app.route('/users', methods=['GET', 'POST'])  # Define a route for '/users' that supports both GET and POST requests
def create_user():
    print(request.method)  # Print the HTTP method
    print(request.form)  # Print the form data
    if request.method == 'POST':  # If the request is a POST request
        first_name = request.form.get('first_name')  # Retrieve the value of the 'first_name' field from the form
        last_name = request.form.get('last_name')  # Retrieve the value of the 'last_name' field from the form

        if first_name and last_name:  # If both 'first_name' and 'last_name' have values
            try:
                conn = mysql.connect()  # Establish a connection to the MySQL database
                cursor = conn.cursor()  # Create a cursor object to execute SQL queries

                # Insert user details into the database
                query = "INSERT INTO users (first_name, last_name) VALUES (%s, %s)"
                cursor.execute(query, (first_name, last_name))  # Execute the SQL query with the user details
                conn.commit()  # Commit the changes to the database


                cursor.close()  # Close the cursor
                conn.close()  # Close the database connection

                return 'User details stored successfully', 201  # Return a success message
            except Exception as e:
                print('Error storing user details:', str(e))  # Print the error message
                return 'Internal Server Error', 500  # Return an error message
        else:
            return 'Missing first name or last name', 400  # Return an error message if either 'first_name' or 'last_name' is missing

    return render_template('index.html')  # Render the 'index.html' template for GET requests

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Start the Flask application on host '0.0.0.0' and port 5000
