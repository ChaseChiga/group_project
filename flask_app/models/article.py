from group_project.flask_app.config.mysqlconnector import (
    MySQLConnection,
    connectToMySQL,
)
from group_project.flask_app.models.user import User
from flask import flash
import re


class Article:
  
    DB = "group_project_schema"

    def __init__(self, data):
        self.id = data.get("id")
        self.title = data.get("article_name")
        self.content = data.get("article_content")
        self.catagory = data.get("catagory")

        self.user_id = data.get("user_id")
        self.creator = None

    # CREATE
    @classmethod
    def save_article(cls, data):
        query = """ 
                INSERT INTO articles (title, content, catagory, user_id)
                VALUE (%(title)s,%(content)s,%(catagory)s,%(user_id)s)
                """
        results = MySQLConnection(cls.DB).query_db(query, data)
        return results

    @classmethod
    def checked_favorite(cls, data):
        # inputs: session['user_id'] & <int:{{"article"id}}
        query = """
                SELECT *
                FROM favorites
                WHERE user_id = %(user_id)s
                AND article_id = %(article_id)s
                """
        results = MySQLConnection(cls.DB).query_db(query, data)
        if results:
            return False
        return results

        # contollers code notes:
        # if Account.checked_favorites(user_id):
        # Before user liking this article we have to check
        # if they have like the article already
        # "if true we have to delete/ unfavorite it"
        # Account.unfavorite_article
        # else:
        #  Account.favorite_article

        # Front end & Controller notes:
        # Is it possible where we can have the articles that have been favorited by the user
        # to have an visual indecator?
        # Ryan's theory code theory
        # Two ways we can do it:
        # One use Article.checked_favorite if runs true. Have the favorite updated

    @classmethod
    def favorite_article(cls, data):
        query = """ 
                INSERT INTO favorites (user_id,article_id)
                VALUE (%(user_id)s,%(articles_id)s)
                """
        results = MySQLConnection(cls.DB).query_db(query, data)
        return results

    @classmethod
    def unfavorite_article(cls, data):
        query = """ 
                DELETE
                FROM favorites
                WHERE user_id = %(user_id)s
                AND
                articles_id = %(article)s
                """
        results = MySQLConnection(cls.DB).query_db(query, data)
        return results

    # READ
    # @classmethod
    # def show_all_articles(cls):
    #     # This will display all articles, the author, and the amount of likes they gathered
    #     query = """
    #             SELECT articles.id, articles.title AS 'article_name',articles.catagory, articles.content AS 'article_content', users.first_name, users.last_name, COUNT(favorites.user_id) AS 'likes_counter'
    #             FROM articles
    # 			LEFT JOIN favorites ON articles.id = favorites.article_id
    #             JOIN users ON users.id = articles.user_id
    #             group BY articles.id, articles.title,articles.catagory, articles.content, users.first_name
    #               """
    #     results = MySQLConnection(cls.DB).query_db(query)
    #     if not results:
    #     # This will premature stop the code if there are no articles made if a user logs in
    #         return results
    #     post = cls(results[0])
    #     for details in results:
    #         articles_post = {

    #             "title": details["article_name"],
    #             "content": details["article_content"],
    #             "catagory": details["catagory"],
    #             "first_name": details["first_name"],
    #             "last_name": details["last_name"],
    #             "likes_counter": details["likes_counter"],
    #             "user_id": details["id"]
    #         }
    #     post.articles.append(User(articles_post))
    #     return results

    # @classmethod
    # def one_article(cls, data):
    #     query = """
    #             SELECT articles.id, articles.title,articles.catagory, articles.content, users.first_name,users.last_name, COUNT(favorites.user_id) AS 'likes_counter'
    #             FROM articles
    # 			LEFT JOIN favorites ON articles.id = favorites.article_id
    #             JOIN users ON users.id = articles.user_id
    #             WHERE articles.id = %(id)s
    #             group BY articles.id, articles.title,articles.catagory, articles.content, users.first_name
    #             """
    #     results = MySQLConnection(cls.DB).query_db(query, data)
    #     post = cls(results[0])
    #     for details in results:
    #         articles_post = {
    #             "title": details["article_name"],
    #             "content": details["article_content"],
    #             "catagory": details["catagory"],
    #             "first_name": details["first_name"],
    #             "last_name": details["last_name"],
    #             "likes_counter": details["likes_counter"],
    #         }
    #     post.articles.append(User(articles_post))
    #     return results[0]

    @classmethod
    def get_all(cls):
        query = """ 
                SELECT articles.id, articles.title AS 'article_name',articles.catagory, articles.content AS 'article_content', users.id AS 'user_id', users.first_name, users.last_name, users.email, users.password, COUNT(favorites.user_id) AS 'likes_counter' 
                FROM articles
				LEFT JOIN favorites ON articles.id = favorites.article_id
                JOIN users ON users.id = articles.user_id
                group BY articles.id, articles.title,articles.catagory, articles.content, users.first_name
                  """
        results = connectToMySQL(cls.DB).query_db(query)
        print("results")
        print(results)
        all_articles = []

        for r in results:
            article = cls(r)
            article.creator = User(
                {
                    "id": r["user_id"],
                    "first_name": r["first_name"],
                    "last_name": r["last_name"],
                    "email": r["email"],
                    "password": r["password"],
                }
            )
            all_articles.append(article)

        print("hi")
        print(all_articles)
        return all_articles

    @classmethod
    def get_by_id(cls, id):
        query = """
                SELECT articles.id, articles.title AS 'article_name', articles.catagory, articles.content AS 'article_content', articles.user_id, users.first_name,users.last_name, users.email,users.password, COUNT(favorites.user_id) AS 'likes_counter' 
                FROM articles
				LEFT JOIN favorites ON articles.id = favorites.article_id
                JOIN users ON users.id = articles.user_id
                WHERE articles.id = %(id)s
                group BY articles.id, articles.title,articles.catagory, articles.content, users.first_name
                """
        data = {"id": id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None


        article_data = results[0]
        article = cls(article_data)
        print("value to rturn is", article)

        user_data = {
            "id": article_data["user_id"],
            "first_name": article_data["first_name"],
            "last_name": article_data["last_name"],
            "email": article_data["email"],
            "password": article_data["password"],
        }
        article.creator = User(user_data)

        return article

    # UPDATE
    @classmethod
    def update_article(cls, data):
        query = """ 
                UPDATE articles
                SET title = %(title)s,
                catagory = %(catagory)s,
                content = %(content)s
                WHERE articles.id = %(id)s 
                """

        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    # DELETE
    # controllers notes:
    # To detele an article we need to delete the likes FIRST that are assocated with with the article
    # Tried to run two queries in one method, but I keep getting errors

    # @classmethod
    # def delete_favorties(cls, data):
    #     query = """ 
    #             DELETE FROM favorites
    #             WHERE article_id = %(id)s
    #             """
    #     results = connectToMySQL(cls.DB).query_db(query, data)
    #     return results

    # @classmethod
    # def delete_article(cls, data):
    #     query = """ 
    #             DELETE FROM articles
    #             WHERE id = %(id)s
    #             """
    #     results = connectToMySQL(cls.DB).query_db(query, data)
    #     return results


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM articles WHERE articles.id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)

    # Static methods

    @staticmethod
    def validate_article(article):
        is_valid = True
        if len(article["title"]) < 1:
            flash("Title is required")
            is_valid = False
        if len(article["content"]) < 1:
            flash("Please provided your article details")
        elif len(article["content"]) > 500:
            flash("Max Character limit is 500")
            is_valid = False
        if len(article["catagory"]) < 1:
            flash("Please select catagory")
            is_valid = False

        return is_valid
