from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route('/info')
def info():
    return render_template("templates/app-templates/index.html")

@app.route('/')
def main():
    return "<h1>Blog Post Manager</h1>"

if __name__ == "__main__":
    app.run()
