from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
import json
import mysql.connector

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app)
host = "localhost"
user = "root"
password = "root1234"
db = "flaskdb"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/api/users")
def read():
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    print(myresult)
    return make_response(jsonify(myresult), 200)


@app.route("/api/users/<id>")
def readbyid(id):
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM users WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    print(myresult)
    return make_response(jsonify(myresult), 200)


@app.route("/api/users", methods=["POST"])
def create():
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    val = (data["name"], data["email"], data["password"])
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(
        jsonify({"message": "User created", "id": mycursor.lastrowid}), 200
    )


@app.route("/api/users/<id>", methods=["PUT"])
def update(id):
    data = request.get_json()
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "UPDATE users SET name = %s, password = %s WHERE id = %s"
    val = (data["name"], data["password"], id)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({"message": "User update", "data": data}), 200)


@app.route("/api/users/<id>", methods=["DELETE"])
def delete(id):
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "DELETE FROM users WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return make_response(jsonify({"message": "User detele", "id": id}), 200)


if __name__ == "__main__":
    app.run(debug=True)
