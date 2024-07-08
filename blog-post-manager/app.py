from glob import glob
import os

from flask import Flask, render_template, abort, url_for
from markupsafe import escape

app = Flask(__name__)

class BlogPost:
    def __init__(self):
        pass

    @staticmethod
    def list_blog_posts():
        return glob(os.path.join(os.path.dirname(__file__), "blog-posts", "*", ""))

#Stuff
@app.route('/info')
def info():
    return render_template("info.html")


@app.route('/posts/<string>')
def edit_post(post_name):
    if post_name not in BlogPost.list_blog_posts():
        abort(404) #TODO: make error page more user-friendly

# Main
@app.route('/')
def main():
    return render_template("info.html", post_names=BlogPost.list_blog_posts())

if __name__ == "__main__":
    app.run()
