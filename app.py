from flask import jsonify, Flask, render_template, request, redirect, session
import csv
import os

app = Flask(__name__)
app.secret_key = "secret123"


# Read network data
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

def read_alerts():
    alerts = []
    try:
        with open("alerts.csv", "r") as f:
            lines = f.readlines()

        for line in lines[1:]:  # skip header
            alerts.append(line.strip().split(","))
    except:
        pass

    return alerts

# 🔐 LOGIN ROUTE (UPDATED)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            with open("users.csv", "r") as f:
                users = f.readlines()

            for user in users[1:]:  # skip header
                u, p = user.strip().split(",")

                if u == username and p == password:
                    session["logged_in"] = True
                    session["user"] = username
                    return redirect("/dashboard")

        except:
            pass

        return "Invalid credentials ❌"

    return render_template("login.html")


# 📝 REGISTER ROUTE
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with open("users.csv", "a") as f:
            f.write(f"{username},{password}\n")

        return redirect("/")

    return render_template("register.html")

@app.route("/data")
def get_data():
    data = read_data()
    alerts = read_alerts()
    return jsonify ({
        "data": data,
        "alerts": alerts
    })

# 📊 DASHBOARD
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")

    data = read_data()
    alerts = read_alerts()

    return render_template("index.html", data=data, alerts=alerts)


# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# 🚀 RUN APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
