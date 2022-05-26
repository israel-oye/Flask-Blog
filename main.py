from flask import Flask, render_template
import requests

app = Flask(__name__)

API_ENDPOINT = "https://api.npoint.io/63fc6636a20c63add2ab"

blog_stories = requests.get(API_ENDPOINT).json()



@app.route("/")
def home_page():
    return render_template("index.html", all_posts=blog_stories)


@app.route("/templates/<nav_page>")
def navigation(nav_page):
    return render_template(f"{nav_page}.html")


@app.route("/template/post<int:num>")
def return_post(num):

    requested_story = None

    for blog_post in blog_stories:
        if blog_post['id'] == num:
            requested_story = blog_post

    return render_template("post.html", requested_post=requested_story)



if __name__ == "__main__":
    app.run(debug=True)