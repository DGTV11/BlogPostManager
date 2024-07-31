# Blog Post Manager
## Description
This is a blog post manager to help you post, delete, upload and edit your posts on Github Pages using GUI! 
This is intended for lazy people like us who want a cool blog but have no time or energy to code one themselves!
## Installing
1) Install python dependencies
```sh
pip3 install -r requirements.txt
```

## Usage
1) From the BlogPostManager folder, run the following command:
```sh
flask --app blog-post-manager/app.py run --host=127.0.0.1
```

2) Open whatever url:port link that is opened up by Flask 
Usually, its localhost

## How to use the application
1) Home page
This page will display all of your blog posts (will be empty at the start) 
To make a new blog post, type a new name for that blogpost in the textbar 
"Post title" and click "Create new blog post" 
After creating your blog post, click on the post name, which will brinmg you to the editor
2) 