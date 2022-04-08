import flask
from flask import Flask, request, render_template, redirect
import sqlite3

conn = sqlite3.connect("Hospital.db", check_same_thread=False)
cursor = conn.cursor()

listOfTables= conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='patient' ").fetchall()

if listOfTables!=[]:
    print("Table Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE patient(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT, 
                            phone INTEGER, 
                            age INT, 
                            address TEXT,   
                            dob INT, 
                            place TEXT, 
                            pincode INT); ''')
print("Table has created")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        getUsername = request.form["username"]
        getppass = request.form["password"]

        if getUsername == "admin":
            if getppass == "12345":
                return redirect("/studentadd")
    return render_template("login.html")


@app.route("/studentadd", methods = ["GET","POST"])
def studentadd():

    if request.method == "POST":
        getname = request.form["name"]
        getphone = request.form["phone"]
        getage = request.form["age"]
        getaddress = request.form["address"]
        getdob = request.form["dob"]
        getplace = request.form["place"]
        getpincode = request.form["pincode"]

        print(getname)
        print(getphone)
        print(getage)
        print(getaddress)
        print(getdob)
        print(getplace)
        print(getpincode)
        try:
            conn.execute("INSERT INTO patient(name, phone, age, address, dob, place, pincode)VALUES('"+getname+"','"+getphone+"','"+getage+"','"+getaddress+"','"+getdob+"','"+getplace+"','"+getpincode+"')")
            print("SUCCESSFULLY INSERTED!")
            conn.commit()
            return redirect('/viewall')
        except Exception as e:
            print(e)

    return render_template("dashboard.html")

@app.route("/viewall")
def viewall():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient")
    result = cursor.fetchall()
    return render_template("viewall.html",patient=result)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        getname = request.form["name"]
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient WHERE name = '"+getname+"' ")
        result = cursor.fetchall()
        return render_template("search.html", patient=result)
    return render_template("find.html")


@app.route("/delete", methods =['GET','POST'])
def delete():
        if request.method == "POST":
            getname = request.form["name"]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patient WHERE name = '" + getname + "' ")
            conn.commit()
        return render_template("delete.html")


@app.route("/update", methods = ['GET','POST'])
def update():
        if request.method == "POST":
            getname = request.form["name"]
            getphone = request.form["phone"]
            getage = request.form["age"]
            getaddress = request.form["address"]
            getdob = request.form["dob"]
            getplace = request.form["place"]
            getpincode = request.form["pincode"]


            conn.execute(
                "UPDATE patient SET phone = '" + getphone + "',age='" + getage + "', address = '" + getaddress + "', dob = '" + getdob + "', place= '" + getplace + "', pincode = '" + getpincode + "' WHERE name = '" + getname + "' ")
            print("successfully Updated !")
            conn.commit()
            return redirect("/viewall")
        return render_template("update.html")

@app.route("/cardview")
def cardview():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient")
    result = cursor.fetchall()
    return render_template("cardview.html",patient=result)


if(__name__) == "__main__":
    app.run(debug=True)