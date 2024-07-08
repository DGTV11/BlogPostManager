from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Blog Post Manager</h1>"

if __name__ == "__main__":
    app.run()
