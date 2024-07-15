from glob import glob
from uuid import uuid4
import os, configparser, shutil, markdown

from flask import Flask, url_for, redirect, request, render_template, abort, flash

from markupsafe import escape

app = Flask(__name__)


class BlogPostHelpers:
    @staticmethod
    def list_blog_post_ids():
        blog_post_filepaths = glob(
            os.path.join(os.path.dirname(__file__), "blog-posts", "*", "")
        )
        blog_post_id_list = list(
            map(lambda s: os.path.basename(os.path.split(s)[0]), blog_post_filepaths)
        )
        return blog_post_id_list


# Stuff
@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/posts/<postid>", methods=("GET", "POST"))
def posts(postid):  # check GH Project for TODO list (to fix this)
    if postid not in BlogPostHelpers.list_blog_post_ids():
        abort(404)  # TODO: make error page more user-friendly

    blog_post_folder_path = os.path.join(os.path.dirname(__file__), "blog-posts", postid)

    if request.method == "POST":
        if request.form["title"] != None:
            pass

    blog_post_folder_path = os.path.join(os.path.dirname(__file__), "blog-posts", postid)
    with open(os.path.join(blog_post_folder_path, "content.md"), "r") as f:
        postcontent = f.read()
    
    # initialise styles.css (create it in same directory as config.ini and content.md) with DEFAULT styles, add persistence to BASIC style editor (convert GUI stuffs to css file also plz add `system-ui` font and support for google fonts)
    with open(os.path.join(blog_post_folder_path, "styles.css"), 'w+') as f:
        font_color = request.cookies.get('font-color') or '#000000'
        font_family = request.cookies.get('font-family') or 'Arial'
        font_size = request.cookies.get('font-size') or '16px'
        css = f"""
            #preview {{
            color: {font_color};
            font-family: {font_family};
            font-size: {font_size};                   
        }}
        """

        f.write(css)
    

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "blog-posts", postid, "config.ini"))
    postname = config['NAME']['post_name']

    return render_template("editor.html", post_name=postname, post_content=postcontent)

def get_bp_names_from_bp_ids(ids):
    bp_names = []
    for id in ids:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "blog-posts", id, "config.ini"))
        bp_names.append(config['NAME']['post_name'])

    return bp_names

# Main
@app.route("/", methods=("GET", "POST"))
def main():
    if request.method == "POST": # CREATES NEW POST
        match request.form["btn"]:
            case "Create new blog post":
                title = request.form["title"]
                if title == "":
                    flash("Title is required!")

                post_id = f"{uuid4().hex}0{uuid4().hex}"
                while post_id in BlogPostHelpers.list_blog_post_ids():
                    post_id = f"{uuid4().hex}0{uuid4().hex}"

                blog_post_folder_path = os.path.join(os.path.dirname(__file__), "blog-posts", post_id)
                os.mkdir(blog_post_folder_path)

                with open(os.path.join(blog_post_folder_path, "config.ini"), 'w') as f:
                    config = configparser.ConfigParser()
                    config['NAME'] = {'post_name': title}
                    config['EDITOR'] = {'isAdvancedMode': False}
                    config.write(f)

                with open(os.path.join(blog_post_folder_path, "content.md"), 'w+') as f:
                    f.write('## Hello, world!')
            case "Delete post": # DELETES POST
                post_id = request.form["pst_id"]
                shutil.rmtree(
                    os.path.join(os.path.dirname(__file__), "blog-posts", post_id)
                )

    all_blog_post_ids = BlogPostHelpers.list_blog_post_ids()
    return render_template("index.html", post_ids_n_names={id: name for id, name in zip(all_blog_post_ids, get_bp_names_from_bp_ids(all_blog_post_ids))})


if __name__ == "__main__":
    app.run()
