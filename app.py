from flask import Flask,jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2025projectSW#'
app.config['MYSQL_DATABASE_DB'] = 'task4'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

conn = mysql.connect()
cursor =conn.cursor()


@app.route('/hello/<name>')
def hello(name):
    return jsonify({"response":f"Hello, {name}!"})


@app.route('/add/<name>/<score>')
def add(name,score):
    query = f"INSERT INTO user (NAME , SCORE) VALUES ('{name}' , {score});"
    cursor.execute(query)
    conn.commit()
    return jsonify({"status":"User added successfully"})


@app.route('/show/<name>')
def get_score(name):
    query = f"SELECT score FROM USER WHERE NAME = '{name}' "
    cursor.execute(query)
    score = cursor.fetchone()
    if (score == None):
        return jsonify({"status":"User doesn't exist"}), 404
    else:
        return jsonify({"score":int(score)})
    


# user go to this endpoint /get/<name>
# search for name in database
#  if found, return name and score
#  if not, return 404 error


if __name__ == '__main__':
    app.run(debug=True)

# app.run()