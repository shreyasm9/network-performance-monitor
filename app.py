
from flask import Flask, render_template
import csv

app = Flask(__name__)

def read_data():
    data = []
    try:
        with open("data/network_log.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data

@app.route("/")
def index():
    data = read_data()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
