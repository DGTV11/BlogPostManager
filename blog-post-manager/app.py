from glob import glob
import os
import markdown
from flask import Flask, url_for, request, render_template, abort, flash

from markupsafe import escape

app = Flask(__name__)


class BlogPost:  # the blog post object
    def __init__(self, date, title, content):
        date = self.date
        title = self.title
        content = self.content

    @staticmethod
    def list_blog_posts():
        blog_post_filepaths = glob(
            os.path.join(os.path.dirname(__file__), "blog-posts", "*", "")
        )
        blog_post_name_list = list(
            map(lambda s: os.path.basename(os.path.split(s)[0]), blog_post_filepaths)
        )
        return blog_post_name_list


# Stuff
@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/posts/<postname>", methods=("GET", "POST"))
def posts(postname):  # check GH Project for TODO list (to fix this)
    if postname not in BlogPost.list_blog_posts():
        abort(404)  # TODO: make error page more user-friendly

    return render_template("form.html", post_name=postname)


# Main
@app.route("/", methods=("GET", "POST"))
def main():
    if request.method == "POST":
        match request.form["btn"]:
            case "Create new blog post":
                title = request.form["title"]
                if title == "":
                    flash("Title is required!")
                os.mkdir(os.path.join(os.path.dirname(__file__), "blog-posts", title))
            case "Delete post":
                post_name = request.form["post_name"]
                os.rmdir(
                    os.path.join(os.path.dirname(__file__), "blog-posts", post_name)
                )

    return render_template("index.html", post_names=BlogPost.list_blog_posts())


if __name__ == "__main__":
    app.run()
