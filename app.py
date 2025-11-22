from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/story")
def story():
    return render_template("story.html")

@app.route("/experiences")
def experiences():
    return render_template("experiences.html")

@app.route("/achievements")
def achievements():
    return render_template("achievements.html")

@app.route("/papers")
def papers():
    return render_template("papers.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/ramblings")
def ramblings():
    return render_template("ramblings.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/perceptrons")
def perceptrons():
    return render_template("perceptrons.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
