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
        blog_post_filepaths = glob(os.path.join(os.path.dirname(__file__), "blog-posts", "*", ""))
        blog_post_name_list = list(map(lambda s: os.path.basename(os.path.split(s)[0]), blog_post_filepaths))
        return blog_post_name_list


# Stuff
@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/posts/<postname>", methods=("GET", "POST"))
def posts(postname): # go through integration hell later
    if postname not in BlogPost.list_blog_posts():
        abort(404)  # TODO: make error page more user-friendly
    if request.method == "POST":
        pass

    return render_template("form.html", post_name=postname)
    print(f"New title: {new_title}, New content: {new_content}")



# Main
@app.route("/", methods=("GET", "POST"))
def main():
    if request.method == "POST":  # TODO: FIX ME!!!
        title = request.form["title"]
        if not title:
            flash("Title is required!")
            redirect(url_for('main'))
        os.mkdir(os.path.join(os.path.dirname(__file__), "blog-posts", title))
        
    return render_template("index.html", post_names=BlogPost.list_blog_posts())

from flask import Flask, render_template, Response, request, redirect, url_for
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html');

def move_forward():
    #Moving forward code
    print("Moving Forward...")

if __name__ == "__main__":
    app.run()
