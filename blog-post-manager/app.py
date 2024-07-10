from glob import glob
import os

from flask import Flask, url_for, request, render_template, abort, flash

from markupsafe import escape

app = Flask(__name__)


class BlogPost: # the blog post object
    def __init__(self, date, title, content):
        date = self.date
        title = self.title
        content = self.content

    @staticmethod
    def list_blog_posts():
        return glob(os.path.join(os.path.dirname(__file__), "blog-posts", "*", ""))


# Stuff
@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/posts/<string>", methods=("GET", "POST"))
def edit_post(post_name):
    if post_name not in BlogPost.list_blog_posts():
        abort(404)  # TODO: make error page more user-friendly
    if request.method == "POST":
        request.form['title'] = post_name['title']
        request.form['content'] = post_name['content']
        new_title = request.form["title"]
        new_content= request.form["content"]
        
        return

    return render_template("form.html", post_name=post_name)
    print(f"New title: {new_title}, New content: {new_content}")



# Main
@app.route("/", methods=("GET", "POST"))
def main():
    if request.method == "POST":  # TODO: FIX ME!!!
        title = escape(request.form["title"].split())
        if not title:
            flash("Title is required!")

    return render_template("index.html", post_names=BlogPost.list_blog_posts())


if __name__ == "__main__":
    app.run()
