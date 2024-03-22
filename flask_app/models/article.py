from flask_app.config.mysqlconnector import MySQLConnection
from flask_app.models.user import User
from flask import flash
import re


class Article:
    DB = 'Group_project_schema'
    def __init__(self,data):
        self.id = data['id']
        self.title= data['title']
        self.content = data['content']
        self.catagory = data['catagory']
        self.articles = []

    # CREATE
    @classmethod
    def save_article(cls,data):
        query = """ 
                INSERT INTO articles (title, content, catagory, user_id)
                VALUE (%(title)s,%(content)s,%(catagory)s,%(user_id)s)
                """
        results = MySQLConnection(cls.DB).query_db(query, data)
        return results
    

    @classmethod
    def checked_favorite(cls,data):
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
            #else:
                #  Account.favorite_article
        
        # Front end & Controller notes:
        # Is it possible where we can have the articles that have been favorited by the user
            # to have an visual indecator?
            # Ryan's theory code theory
                # Two ways we can do it:
                # One use Article.checked_favorite if runs true. Have the favorite updated
        
    @classmethod
    def favorite_article(cls,data):
        query = """ 
                INSERT INTO favorites (user_id,article_id)
                VALUE (%(user_id)s,%(articles_id)s)
                """
        results = MySQLConnection(cls.DB).query_db(query, data)
        return results
        
    @classmethod
    def unfavorite_article(cls,data):
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
    @classmethod
    def show_all_articles(cls,data):
        # This will display all articles, the author, and the amount of likes they gathered
        query = """ 
                SELECT articles.id, articles.title AS 'article_name',articles.catagory, articles.content AS 'article_content', users.first_name, users.last_name, COUNT(favorites.user_id) AS 'likes_counter' 
                FROM articles
				LEFT JOIN favorites ON articles.id = favorites.article_id
                JOIN users ON users.id = articles.user_id
                group BY articles.id, articles.title,articles.catagory, articles.content, users.first_name
                """
        results = MySQLConnection(cls.DB).query_db(query, data)
        if results == (): # This will premature stop the code if there are no articles made if a user logs in
            return results
        post = cls(results[0])
        for details in results:
            articles_post = {
                'title': details['tiles'],
                'catagory': details['catagory'],
                'content': details['content'],
                'first_name': details['first_name'],
                'last_name': details['last_name'],
                'favorites': details['favorties']
            }
        post.articles.append(User(articles_post))
        return results
    
    @classmethod
    def one_article(cls,data):
        query = """
                SELECT articles.id, articles.title,articles.catagory, articles.content, users.first_name,users.last_name, COUNT(favorites.user_id) AS 'favorites' 
                FROM articles
				LEFT JOIN favorites ON articles.id = favorites.article_id
                JOIN users ON users.id = articles.user_id
                WHERE articles.id = %(id)s
                group BY articles.id, articles.title,articles.catagory, articles.content, users.first_name
                """
        results = MySQLConnection(cls.DB).query_db(query, data)
        post = cls(results[0])
        for details in results:
            articles_post = {
                'title': details['tiles'],
                'catagory': details['catagory'],
                'content': details['content'],
                'first_name': details['first_name'],
                'last_name': details['last_name'],
                'favorites': details['favorties']
            }
        post.articles.append(User(articles_post))
        return results[0]
    
    # UPDATE
    @classmethod
    def update_article(cls,data):
        query = """ 
                UPDATE articles
                SET title = %(title)s, content = %(content)s,
                catagory = %(catagory)s
                WHERE id = %(id)s 
                """
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results
    

    # DELETE
    # controllers notes:
        # To detele an article we need to delete the likes FIRST that are assocated with with the article
        # Tried to run two queries in one method, but I keep getting errors
    
    @classmethod
    def delete_favorties(cls,data):
        query = """ 
                DELETE FROM favorites
                WHERE article_id = %(id)s
                """
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results

    @classmethod
    def delete_article(cls,data):
        query = """ 
                DELETE FROM articles
                WHERE id = %(id)s
                """
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results

    # Static methods

    @staticmethod
    def validate_article(form):
        is_valid = True
        if len(form['title']) < 1:
            flash('Title is required')
            is_valid = False
        if len(form['catagory'])  < 1:
            flash('Please select catagory')
        if len(form['content']) < 1:
            flash('Please provided your article details')
        if len(form['content']) > 500:
            flash('Max Character limit is 500')
        return is_valid
    