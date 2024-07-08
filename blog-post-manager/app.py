from glob import glob
import os

from flask import Flask, url_for, request, render_template, abort

from markupsafe import escape

app = Flask(__name__)

class BlogPost:
    def __init__(self):
        pass

    @staticmethod
    def list_blog_posts():
        return glob(os.path.join(os.path.dirname(__file__), "blog-posts", "*", ""))

@app.route('/info')
def info():
    return render_template(os.path.join(os.path.dirname(__file__), "templates", "app-templates", "info.html"))

@app.route('/')
def main():
    get_post_route = lambda pname: url_for('posts', pname) 
    post_tags = [f"<a href='{get_post_route(post_name)}'>{post_name}</a>" for post_name in BlogPost.list_blog_posts()]
    return f"""<h1>Blog Post Manager</h1>
    <h2>Blog Posts</h2>
    """ + '\n'.join(post_tags)

@app.route('/posts/<string>', methods=["GET", "POST"])
def edit_post(post_name):
    if post_name not in BlogPost.list_blog_posts():
        abort(404) #TODO: make error page more user-friendly
    if request.method == "POST":
        title = request.form["title"]
        content= request.form["content"]
        return

    return render_template("form.html")

if __name__ == "__main__":
    app.run()
