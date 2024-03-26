from flask import render_template, redirect, request, session, flash

from flask_app.models.article import Article
from flask_app.models.user import User


from flask_app import app
from datetime import datetime


from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/dashboard")
def get_all_articles():
    if "user_id" not in session:
        return redirect("/")
    articles = Article.get_all()
    print("this")
    print(articles)
    user_id = session['user_id']
    print(f"!!!!!!!!!{user_id}!!!!!!!!!!")
    return render_template("index.html", articles=articles, user_id = user_id)


@app.route("/home")
def home():
    return render_template("login.html")


@app.route("/create")
def create():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    user = User.get_by_id(user_id)  
    return render_template("new_blog.html", user=user)


@app.route("/create", methods=["POST"])
def add_blog():
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]

    if not Article.validate_article(request.form):
        return redirect("/create")

    data = {
        "title": request.form["title"],
        "catagory": request.form["catagory"],
        "content": request.form["content"],
        "user_id": user_id,
    }

    Article.save_article(data)

    print(data)
    return redirect("/dashboard")

@app.route("/articles/<int:article_id>")
def get_one(article_id):
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]

    article = Article.get_by_id(article_id)
    print("inside display page")
    print(article)
    return render_template("show.html", article=article)

# @app.route("/create", methods=["POST"])
# def create_blog():
#     if "user_id" not in session:
#         return redirect("/")

#     # Fetch user information from session or database based on user_id
#     user = User.get_by_id(session["user_id"])

#     # Pass user information to the template
#     return render_template("new_blog.html", user=user)

@app.route("/articles/edit/<int:article_id>")
def edit_article(article_id):
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    article = Article.get_by_id(article_id)
    print("article is",article)
    return render_template("edit.html", article=article)


@app.route("/articles/edit/<int:article_id>", methods=["POST"])
def update(article_id):
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]

    if not Article.validate_article(request.form):
        return redirect(f"/articles/edit/{article_id}")

    article_data = {
        "id": article_id,
        "title": request.form["title"],
        "catagory": request.form["catagory"],
        "content": request.form["content"],
        "user_id": user_id,
    }


    Article.update_article(article_data)
    return redirect(f"/articles/{article_id}")

@app.route("/article/<int:article_id>/destroy")
def delete_article(article_id):
    print("inside destroy")
    Article.delete(article_id)
    return redirect("/dashboard")

@app.route("/article/like", methods=["POST"])
def add_like():
    if 'user_id' not in session:
        return redirect('/logout')
    print(request.form)
    print(Article.check_favorite(request.form))
    if Article.check_favorite(request.form) != True:
        Article.favorite_article(request.form)
    else:
        Article.unfavorite_article(request.form)
    return redirect('/dashboard')