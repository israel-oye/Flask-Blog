from flask import Flask, redirect, render_template, request, url_for
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_ENDPOINT = os.getenv("API_ENDPOINT")


blog_stories = requests.get(API_ENDPOINT).json()



@app.route("/", methods=["GET", "POST"])
def home_page():    
    return render_template("index.html", all_posts=blog_stories)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/contact", methods=['POST', 'GET'])
def contact_page():
    if request.method == 'POST':
        user_name = request.form['name']
        user_mail = request.form['email']
        user_number = request.form['phone']
        user_msg = request.form['message']

        send_mail(name=user_name, mail=user_mail, number=user_number, msg=user_msg)

        return render_template("contact.html", h1_entry="Message sent")
    else:
        return render_template("contact.html", h1_entry="Contact Me")

def send_mail(name, mail, number, msg):
    from smtplib import SMTP
    load_dotenv()

    email = os.getenv("EMAIL")
    pwd = os.getenv("PWD")
    message = f"Subject: New Message from Blogasaurus\n\nName:{name}\nMail:{mail}\nNumber:{number}\nMessage:{msg}"

    with SMTP(host="smtp.gmail.com") as connection:
        connection.starttls()

        connection.login(user=email, password=pwd)
        connection.sendmail(from_addr=email, to_addrs=email, msg=message)

@app.route("/post<int:num>")
def return_post(num):

    requested_story = None

    for blog_post in blog_stories:
        if blog_post['id'] == num:
            requested_story = blog_post

    return render_template("post.html", requested_post=requested_story)

@app.route("/login/<mail>&<pwd>")
def logged_in_page(email, passwd):
    return render_template("login.html", mail=email, password=passwd)


if __name__ == "__main__":
    app.run(debug=True)