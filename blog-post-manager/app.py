import os

from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

def list_blog_posts():
    return list(filter(lambda folder_name: not folder_name.startswith('_'), os.listdir(os.path.join(os.path.dirname(__file__), "blog-posts"))))

@app.route('/info')
def info():
    return render_template(os.path.join(os.path.dirname(__file__), "templates", "app-templates", "info.html"))

@app.route('/')
def main():
    
    return """<h1>Blog Post Manager</h1>

    """

@app.route('/posts/<string>')
def edit_post(post_name):
    

if __name__ == "__main__":
    app.run()
