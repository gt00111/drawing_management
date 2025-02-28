from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("drawing_management.html")

@app.route("/comparsion")
def comparsion():
    return render_template("comparsion.html")

if __name__ == "__main__":
    app.run(debug=True)