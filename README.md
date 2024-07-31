# Blog Post Manager
## Description
This is a blog post manager to help you post, delete, upload and edit your posts on Github Pages using GUI! 
This is intended for lazy people like us who want a cool blog but have no time or energy to code one themselves!
## Installing
1) Install Python 3 and pip

2) From the BlogPostManager folder, install Python dependencies
```sh
pip3 install -r requirements.txt
```

## Usage
1) From the BlogPostManager folder, run the following command:
```sh
flask --app blog-post-manager/app.py run --host=127.0.0.1
```

2) Open the url:port that was opened up by Flask (it's usually `127.0.0.1:5000`)
Usually, its localhost

# How to use the application
## Home page
- This page will display all of your blog posts (will be empty at the start).  
  
- To make a new blog post, type a new name for that blogpost in the textbar, "Post title" and click "Create new blog post"  
- After creating your blog post, click on the post name, which will bring you to the editor.  

- You can access your previous blog posts by clicking the post title.  
## Editor page  
- This is the page where you make your blog post. It will have the default description and content.  

- This page has a markdown editor to allow you to put quotes, italics and much more,  
as well as having the ability to change the fonts and colour of the text in the post.  

- Afterward making your blog, click the 'Save' button at the bottom (so you don't lose your post) and you can return  
to the home page by clicking 'Back to menu'.  

## Export page  
- If you want to export your posts, click the button 'Export' at the bottom of the home page to go to the export page.  
- In the 'Blog name' textfield, you can name your blog (NOT the blog posts, but the name for the blog which will have your blogs posts)
- There is also a navigation bar that you can input the title and the link reference (href), which will be present in the html file at the top of the blog you made. 
- If you have finished your blog, you can download it with the 'Export' button on the right side. It will download the HTML file for your whole blog, where you can put it on Github Pages or anywhere you like!



