from glob import glob
import os, configparser, shutil, markdown

from flask import Flask, url_for, request, render_template, abort, flash

from markupsafe import escape

app = Flask(__name__)


class BlogPostHelpers:
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
    if postname not in BlogPostHelpers.list_blog_posts():
        abort(404)  # TODO: make error page more user-friendly

    blog_post_folder_path = os.path.join(os.path.dirname(__file__), "blog-posts", postname)
    with open(os.path.join(blog_post_folder_path, "content.md"), "r") as f:
        postcontent = f.read()

    return render_template("editor.html", post_name=postname, post_content=postcontent)


# Main
@app.route("/", methods=("GET", "POST"))
def main():
    if request.method == "POST":
        match request.form["btn"]:
            case "Create new blog post":
                title = request.form["title"]
                if title == "":
                    flash("Title is required!")

                blog_post_folder_path = os.path.join(os.path.dirname(__file__), "blog-posts", title)
                os.mkdir(blog_post_folder_path)

                with open(os.path.join(blog_post_folder_path, "config.ini"), 'w') as f:
                    config = configparser.ConfigParser()
                    config['EDITOR'] = {'isAdvancedMode': False}
                    config.write(f)
                with open(os.path.join(blog_post_folder_path, "content.md"), 'w+') as f:
                    f.write('## Hello, world!')
            case "Delete post":
                post_name = request.form["post_name"]
                shutil.rmtree(
                    os.path.join(os.path.dirname(__file__), "blog-posts", post_name)
                )

    return render_template("index.html", post_names=BlogPostHelpers.list_blog_posts())


if __name__ == "__main__":
    app.run()
