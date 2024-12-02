from flask import Flask,jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()

cursor.execute("SELECT * from User")
data = cursor.fetchone()


# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()
    result = [{"id": u[0], "name": u[1], "email": u[2], "age": u[3]} for u in users]
    return jsonify(result)

# Get a single user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM User WHERE id = %s", (id,))
    user = cursor.fetchone()
    if user:
        result = {"id": user[0], "name": user[1], "email": user[2], "age": user[3]}
        return jsonify(result)
    return jsonify({"error": "User not found"}), 404

# Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO User (name, email, age) VALUES (%s, %s, %s)",
        (data['name'], data['email'], data['age']),
    )
    mysql.connection.commit()
    return jsonify({"message": "User added successfully"}), 201

# Update an existing user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE User SET name = %s, email = %s, age = %s WHERE id = %s",
        (data['name'], data['email'], data['age'], id),
    )
    mysql.connection.commit()
    return jsonify({"message": "User updated successfully"})

# Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM User WHERE id = %s", (id,))
    mysql.connection.commit()
    return jsonify({"message": "User deleted successfully"})

# @app.route('/api/data', methods=['GET'])
# def get_data():
#     sample_data = {
#         "name": "Test",
#         "description": "A sample API endpoint returning JSON data",
#         "status": "success"
#     }
#     return jsonify(sample_data)

@app.route('/hello/<name>')
def hello(name):
    return jsonify({"response":f"Hello, {name}!"})
   


if __name__ == '__main__':
    app.run(debug=True)

# app.run()