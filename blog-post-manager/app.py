from glob import glob
from uuid import uuid4
import os, configparser, shutil

from flask import Flask, url_for, request, render_template, abort, send_file, flash
from markupsafe import escape

import markdown

with open(os.path.join(os.path.dirname(__file__), "export-template.html"), 'r') as f:
    EXPORT_TEMPLATE_TXT = f.read()

app = Flask(__name__)
app.config["SECRET_KEY"] = "aslkjhlhkjfdsalkjhfdsha"

def list_blog_post_ids():
    blog_post_filepaths = glob(
        os.path.join(os.path.dirname(__file__), "blog-posts", "*", "")
    )
    blog_post_id_list = list(
        map(lambda s: os.path.basename(os.path.split(s)[0]), blog_post_filepaths)
    )
    return blog_post_id_list

def get_bp_names_from_bp_ids(ids):
    bp_names = []
    for id in ids:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "blog-posts", id, "config.ini"))
        bp_names.append(config['NAME']['post_name'])

    return bp_names

# Stuff
@app.route("/posts/<postid>", methods=("GET", "POST"))
def posts(postid):  # check GH Project for TODO list (to fix this)
    saved = False
    if postid not in list_blog_post_ids():
        abort(404)  # TODO: make error page more user-friendly

    blog_post_folder_path = os.path.join(os.path.dirname(__file__), "blog-posts", postid)

    if request.method == "POST":
        font_color = request.form['font-color']
        font = request.form['font']

        match request.form["btn"]:
            case "Save":
                config = configparser.ConfigParser()
                config.read(os.path.join(blog_post_folder_path, "config.ini"))
                isAdvancedMode = config['EDITOR']['isAdvancedMode']

                with open(os.path.join(blog_post_folder_path, "config.ini"), 'w+') as f:
                    config = configparser.ConfigParser()
                    config['NAME'] = {'post_name': request.form['title']}
                    config['EDITOR'] = {'isAdvancedMode': isAdvancedMode}
                    config.write(f)

                with open(os.path.join(blog_post_folder_path, "content.txt"), 'w') as f:
                    f.write(request.form['content'])
            
                with open(os.path.join(blog_post_folder_path, "description.txt"), 'w') as f:
                    f.write(request.form['desc'])

                with open(os.path.join(blog_post_folder_path, "styles.ini"), 'w') as f:
                    config = configparser.ConfigParser()
                    config['STYLES'] = {'font_color': font_color, 'font': font}
                    config.write(f)

                saved = True
        # The part to reload the stuff back
        config = configparser.ConfigParser()
        config.read(os.path.join(blog_post_folder_path, "styles.ini"))
        font_color = config['STYLES']['font_color']
        font = config['STYLES']['font']
        config.read(os.path.join(os.path.dirname(__file__), "blog-posts", postid, "config.ini"))
        postname = config['NAME']['post_name']

        with open(os.path.join(blog_post_folder_path, "content.txt"), "r") as f:
            postcontent = f.read()

        with open(os.path.join(blog_post_folder_path, "description.txt"), "r") as f:
            postdesc = f.read()   
        return render_template('editor.html', saved=saved, postid=postid, post_name=postname, post_desc=postdesc, post_content=postcontent, font_color=font_color, font_fonty_font_font=font)
        #Apologies, a bit disgusting but well a cool tiny detail no one will notice has been added!
        
    else:
        config = configparser.ConfigParser()
        config.read(os.path.join(blog_post_folder_path, "styles.ini"))
        font_color = config['STYLES']['font_color']
        font = config['STYLES']['font']

    with open(os.path.join(blog_post_folder_path, "content.txt"), "r") as f:
        postcontent = f.read()

    with open(os.path.join(blog_post_folder_path, "description.txt"), "r") as f:
        postdesc = f.read()

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "blog-posts", postid, "config.ini"))
    postname = config['NAME']['post_name']

    return render_template("editor.html", post_name=postname, post_desc=postdesc, post_content=postcontent, font_color=font_color, font_fonty_font_font=font)

other_navbar_links = {}
@app.route("/export", methods=("GET", "POST"))
def export():
    global other_navbar_links #disgusting but oh well
    
    if request.method == "POST":
         match request.form["btn"]:
            case "Export":
                if not request.form["blog_name"].strip():
                     flash("Blog name is required!")
                else:
                    all_blog_post_ids = list_blog_post_ids()
                    all_blog_post_names = get_bp_names_from_bp_ids(all_blog_post_ids)
                    all_blog_post_descriptions = []
                    all_blog_post_contents = []
                    all_blog_post_styles = []

                    for blog_post_id in all_blog_post_ids:
                        blog_post_folder_path = os.path.join(os.path.dirname(__file__), "blog-posts", blog_post_id)

                        with open(os.path.join(blog_post_folder_path, "description.txt"), 'r') as f:
                            all_blog_post_descriptions.append(f.read())

                        with open(os.path.join(blog_post_folder_path, "content.txt"), 'r') as f:
                            all_blog_post_contents.append(markdown.markdown(f.read()))

                        config = configparser.ConfigParser()
                        config.read(os.path.join(blog_post_folder_path, "styles.ini"))
                        font_color = config['STYLES']['font_color']
                        font = config['STYLES']['font']
                        all_blog_post_styles.append(f"color: {font_color}; font-family: {font}, system-ui;")

                    links_to_blog_posts = ""
                    blog_pages = ""
                    styles = ""
                    for blog_post_id, blog_post_name, blog_post_description, blog_post_content, blog_post_style in zip(all_blog_post_ids, all_blog_post_names, all_blog_post_descriptions, all_blog_post_contents, all_blog_post_styles):
                        links_to_blog_posts += f'<section><a class="h3-a" onClick="showPage(\'{blog_post_id}\')">{blog_post_name}</a><p>{blog_post_description}</p></section>\n'
                        blog_pages += f'<div id="{blog_post_id}" class="page"><h1>{blog_post_name}</h2><h3>{blog_post_description}</h3><p style="{blog_post_style}">{blog_post_content}</p></div>\n'

                    right_navbar_links = ""
                    for link_name, link_href in other_navbar_links.items():
                        right_navbar_links += f'<a class="h3-a right-nav" href="{link_name}">{link_name}</a>'

                    export_html = EXPORT_TEMPLATE_TXT.replace("@BLOGNAME@", request.form["blog_name"].strip()).replace("@LINKS_TO_BLOG_POSTS@", links_to_blog_posts).replace("@BLOG_PAGES@", blog_pages).replace('@RIGHT_NAV@', right_navbar_links)

                    with open(os.path.join(os.path.dirname(__file__), 'tmp', 'blog.html'), 'w+') as f:
                        f.write(export_html)

                    return send_file(os.path.join(os.path.dirname(__file__), 'tmp', 'blog.html'), as_attachment=True)
            case "Create new navbar link":
                title = request.form["title"].strip()
                href = request.form["href"].strip()
                if not title:
                    flash("Navbar link title is required!")
 
                elif title in other_navbar_links:
                    flash("Navbar link title must be unique!")
                elif not href:
                    flash("Navbar href is required!")
                else:
                    other_navbar_links[title] = href
            case "Delete navbar link":
                post_name = request.form["link_name"]
                del other_navbar_links[post_name]

    return render_template("export.html", link_names_n_hrefs=other_navbar_links)

# Main

@app.route("/", methods=("GET", "POST"))
def main():
    if request.method == "POST": # CREATES NEW POST
        match request.form["btn"]:
            case "Create new blog post":
                title = request.form["title"].strip()
                if not title:
                    flash("Blog post name is required!")
                else:
                    post_id = f"{uuid4().hex}0{uuid4().hex}"
                    while post_id in list_blog_post_ids():
                        post_id = f"{uuid4().hex}0{uuid4().hex}"

                    blog_post_folder_path = os.path.join(os.path.dirname(__file__), "blog-posts", post_id)
                    os.mkdir(blog_post_folder_path)

                    with open(os.path.join(blog_post_folder_path, "config.ini"), 'w') as f:
                        config = configparser.ConfigParser()
                        config['NAME'] = {'post_name': title}
                        config['EDITOR'] = {'isAdvancedMode': False}
                        config.write(f)

                    with open(os.path.join(blog_post_folder_path, "content.txt"), 'w+') as f:
                        f.write('## Hello, world!')

                    with open(os.path.join(blog_post_folder_path, "description.txt"), 'w+') as f:
                        f.write('Insert description here')

                    # initialise styles.ini (create it in same directory as config.ini and content.txt) with DEFAULT styles, add persistence to BASIC style editor (convert GUI stuffs to css file also plz add `system-ui` font and support for google fonts)
                    with open(os.path.join(blog_post_folder_path, "styles.ini"), 'w') as f:
                        config = configparser.ConfigParser()
                        config['STYLES'] = {'font_color': '#000000', 'font': 'system-ui'}
                        config.write(f)

            case "Delete post": # DELETES POST
                post_id = request.form["pst_id"]
                shutil.rmtree(
                    os.path.join(os.path.dirname(__file__), "blog-posts", post_id)
                )

    all_blog_post_ids = list_blog_post_ids()
    return render_template("index.html", post_ids_n_names={id: name for id, name in zip(all_blog_post_ids, get_bp_names_from_bp_ids(all_blog_post_ids))})


if __name__ == "__main__":
    app.run()
