import os

from flask import Flask, render_template, abort
from markupsafe import escape

app = Flask(__name__)

def list_blog_posts():
    return list(filter(lambda folder_name: not (folder_name.startswith('_') or folder_name.startswith('.')), os.listdir(os.path.join(os.path.dirname(__file__), "blog-posts"))))

@app.route('/info')
def info():
    return render_template(os.path.join(os.path.dirname(__file__), "templates", "app-templates", "info.html"))

@app.route('/')
def main():
    return f"""<h1>Blog Post Manager</h1>
    
    """

@app.route('/posts/<string>')
def edit_post(post_name):
    if post_name not in list_blog_posts():
        abort(404) #TODO: make error page more user-friendly

if __name__ == "__main__":
    app.run()