from flask import Flask, render_template, request, redirect, session
import csv

app = Flask(__name__)
app.secret_key = "secret123"

USERNAME = "admin"
PASSWORD = "admin"

def read_data():
    data = []
    try:
        with open("data/network_log.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except:
        pass
    return data

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == USERNAME and pwd == PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")

    data = read_data()
    print("DEBUG DATA:", data)
    return render_template("index.html", data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
