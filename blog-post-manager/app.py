from glob import glob
from uuid import uuid4
import os, configparser, shutil, markdown

from flask import Flask, url_for, request, render_template, abort, flash

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
        match request.form["btn"]:
            case "Save":
                config = configparser.ConfigParser() # a interface with the config files
                config.read(os.path.join(blog_post_folder_path, "config.ini"))
                isAdvancedMode = config['EDITOR']['isAdvancedMode']

                with open(os.path.join(blog_post_folder_path, "config.ini"), 'w+') as f:
                    config = configparser.ConfigParser()
                    config['NAME'] = {'post_name': request.form['title']}
                    config['EDITOR'] = {'isAdvancedMode': isAdvancedMode}
                    config.write(f)

                with open(os.path.join(blog_post_folder_path, "content.md"), 'w') as f:
                    f.write(request.form['content'])

                with open(os.path.join(blog_post_folder_path, "basic-styles.ini"), 'w') as f:
                    config = configparser.ConfigParser()
                    config['STYLES'] = {'font_color': request.form['font-color'], 'font-family': request.form['font-family'], 'font-size': request.form['font-size']}
                    config.write(f)
            case "Update styles":
                pass
            case "Switch to advanced mode:":
                config = configparser.ConfigParser() # a interface with the config files
                config.read(os.path.join(blog_post_folder_path, "config.ini"))                
                isAdvancedMode = config['EDITOR']['isAdvancedMode']
                if isAdvancedMode:
                    with open(os.path.join(blog_post_folder_path, "content.md"), 'r') as f:
                        md_data = f.read(request.form['content'])
                    html_data = markdown.markdown(md_data)
                    with open(os.path.join(blog_post_folder_path, "content.md"), 'w') as f:
                        f.write(html_data)
                else:
                    pass
            case "Switch to basic mode:":
                config = configparser.ConfigParser() # a interface with the config files
                config.read(os.path.join(blog_post_folder_path, "config.ini"))                
                isAdvancedMode = config['EDITOR']['isAdvancedMode']
                if isAdvancedMode == False:
                  pass
                else:
                    with open(os.path.join(blog_post_folder_path, "content.md"), 'w') as f:
                        f.write(request.form['content'])

    with open(os.path.join(blog_post_folder_path, "content.md"), "r") as f:
        postcontent = f.read()

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

                # initialise basic-styles.ini (create it in same directory as config.ini and content.md) with DEFAULT styles, add persistence to BASIC style editor (convert GUI stuffs to css file also plz add `system-ui` font and support for google fonts)
                with open(os.path.join(blog_post_folder_path, "basic-styles.ini"), 'w') as f:
                    config = configparser.ConfigParser()
                    config['STYLES'] = {'font_color': '#000000', 'font-family': 'system-ui', 'font-size': "16"}
                    config.write(f)

            case "Delete post": # DELETES POST
                post_id = request.form["pst_id"]
                shutil.rmtree(
                    os.path.join(os.path.dirname(__file__), "blog-posts", post_id)
                )

    all_blog_post_ids = BlogPostHelpers.list_blog_post_ids()
    return render_template("index.html", post_ids_n_names={id: name for id, name in zip(all_blog_post_ids, get_bp_names_from_bp_ids(all_blog_post_ids))})


if __name__ == "__main__":
    app.run()
