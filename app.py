from flask import Flask, render_template, request
import os
import mariadb as database
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    return '<h1>{}</h1>' .format(request.form['todoitem'])

if __name__ == '__main__':
    app.run(debug=True)


# Load env vars from current shell env
# (source secret file first: source .secret_env_vars)
username = os.environ.get("dbusername")
password = os.environ.get("dbpassword")

# Connect to MariaDB Platform
try:
    connection = database.connect(
        user = username,
        password = password,
        host = "127.0.0.1",
        port = 3306,
        database = "todo_database"

    )
except database.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cursor = connection.cursor()

# Adding data to database
def add_data(todos_description, is_completed):
    try:
        statement = "INSERT INTO todos (todos_description,is_completed) VALUES (%s, %s)"
        data = (todos_description, is_completed)
        cursor.execute(statement, data)
        connection.commit()
        print("Successfully added entry to database")
    except database.Error as e:
        print(f"Error adding entry to database: {e}")

# Retrieving data from database
def get_data(is_completed):
    try:
      statement = "SELECT todos_description, is_completed FROM todos WHERE is_completed=%s"
      data = (is_completed,)
      cursor.execute(statement, data)
      for (todos_description, is_completed) in cursor:
        print(f"Successfully retrieved {todos_description}, {is_completed}")
    except database.Error as e:
      print(f"Error retrieving entry from database: {e}")

# Verify that your code is running as expected
add_data("test app", 1)
get_data(1)

connection.close()
