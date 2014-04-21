from google.appengine.ext import ndb

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from utils import *

class User(ndb.Model):
    """
    A registered user
    """

    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    #email = ndb.StringProperty()
    joined = ndb.DateTimeProperty(auto_now_add=True)
    group = ndb.StringProperty(required=True)
    college = ndb.StringProperty(required=True)
   

    @classmethod
    def create_user(cls, group, college, username, password):
        """
        Create a new user with the provided credentials,
        and throw an exception if something's wrong
        """

        if not is_username_valid(username):
            raise ValidationError("That's not a valid username.")

        user = cls.query(cls.username==username).fetch()
        if user:
            raise UserError("User already exists!")

        if not is_password_valid(password):
            raise ValidationError("That's not a valid password.")

        

        if group:
            if not is_group_valid(group):
                raise ValidationError("That's not a valid group/individual name. Please select an unique name!")
        new_user = cls(group=group, college=college, username=username, password=encrypt(password)).put()
        return new_user.id()

    @classmethod
    def authenticate(cls, username, password):
        """
        Check if the provided username and password are valid
        """

        try:
            user = cls.query(cls.username==username).fetch()[0]

        except:
            raise UserError("User does not exist!")

        if user.username == username and user.password == encrypt(password):
            return str(user.key.id())
        else:
            raise AuthenticationError("Invalid username/password!")

   

class Post(ndb.Model, blobstore_handlers.BlobstoreUploadHandler):
    """
    Video post by a registered user
    """

    blobKey = ndb.BlobKeyProperty(required=True)
    caption = ndb.StringProperty(required=True)
    author = ndb.KeyProperty(kind='User', required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    #searchval = ndb.StringProperty(required=True)
    #authorid = ndb.IntegerProperty(required=True)

    @classmethod
    def top_posts(cls):
        """
        Returns the most recent 10 posts
        """
        
        top_posts = cls.query().order(-cls.created).fetch()
        return list(top_posts)

    @classmethod
    def create_new(cls, caption, blobKey, user):
        """
        Create a new post
        """

        # if not title or content:
        #   raise ValidationError("Title / content cannot be empty!")
        
        post = cls(caption=caption, blobKey=blobKey, author=user.key).put()

        return post.id()

    


   










