import webapp2
#import urllib

from utils import *

from models import User, Post

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class BaseHandler(webapp2.RequestHandler):
    """
    Base class for view functions, which provides basic rendering 
    funtionalities
    """

    def render(self, template, **kw):
        """
        Render a template with the given keyword arguments
        """

        self.response.out.write(render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """
        Set an encrypted cookie on client's machine
        """

        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val)
            )

    def read_secure_cookie(self, name):
        """
        Read a cookie and check it's integrity
        """

        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def initialize(self, *a, **kw):
        """
        Override the constuctor for adding user information
        when a request comes
        """

        webapp2.RequestHandler.initialize(self, *a, **kw)
        user_id = self.read_secure_cookie('user')
        self.user = user_id and User.get_by_id(int(user_id))

class Home(BaseHandler):
    """
    Render the homepage.
    """

    def get(self):
        """
        For a GET request, render the homepage.
        """

        self.render("home.html", user=self.user, permalink=False)


class downloadVideo(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id))
        #resource = Post.post.blobKey
        resource = post.blobKey
        #resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)


class Permalink(BaseHandler):
    """
    Handle permalink for the posts
    """

    def get(self, post_id):
        """
        For a GET request with a valid post_id, return the post
        Else, return a 404 error
        """
        
        post = Post.get_by_id(int(post_id))

        if post:
            self.render("dashboard.html", user=self.user, posts=[post], video="/download/"+post_id, permalink=True)
        else:
            self.abort(404)



class Login(BaseHandler):
    """
    Handles the login page
    """

    def get(self):
        """
        For a GET request, render the login page
        """

        user = self.user

        if user:
            self.redirect('/dashboard')

        self.render("login.html", user=user)

    def post(self):
        """
        For a POST request, perform the login. If successful, redirect
        to homepage
        """

        username = self.request.get('username')
        password = self.request.get('password')

        try:
            user_id = User.authenticate(username, password)
            self.set_secure_cookie('user', str(user_id))
            self.redirect('/dashboard')
        
        except Exception, e:
            self.render("login.html", user=self.user, error = e)

class Signup(BaseHandler):
    """
    Signup a new user
    """

    def get(self):
        """
        Render the signup page
        """

        user = self.user

        if user:
            self.redirect('/')

        self.render('signup.html', user=user)

    def post(self):
        """
        Create a new user, and redirect to homepage
        """

        username = self.request.get('username')
        password = self.request.get('password')
        group = self.request.get('group')
        college = self.request.get('college')

        try:
            user = User.create_user(group, college, username, password)
            self.render("login.html",
                        success="Great! You are registered! Please log in.", user=user)

        except Exception, e:
            self.render("signup.html", user=self.user, error=e)

class Dashboard(BaseHandler):
    """
    Handle the dashboard NOT COMPLETE
    """

    def get(self):
        """
        For a GET request, return the homepage
        """

        top_posts = Post.top_posts()

        ##if not self.user:
          ##  self.redirect('/login')
        #try:
        self.render("dashboard.html", posts=top_posts, user=self.user, permalink=False)

        #except Exception, e:
         #   self.redirect('/dashboard')

class NewPost(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    """
    Handles all the new video posts
    """

    def get(self):
        """
        Render the form for adding new post
        """
        if not self.user:
            self.redirect('/login')

        upload_url = blobstore.create_upload_url('/upload')
        self.render("newpost.html", uploads=upload_url, user=self.user)

class UploadHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    """
    Handles the upload part
    """    
    
    def post(self):
        """
        Add a new post, and redirect to the permalink page
        """

        if not self.user:
            self.abort(403)


        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
       # if(blob_info):
        #    self.redirect('/dashboard/%s' % blob_info.key())

        caption = self.request.get('caption')
        blobKey = blob_info.key()
        user = self.user
        #author = self.request.get('group')
        #college = self.request.get('college')

        try:
            post_id = Post.create_new(caption=caption, blobKey=blobKey, user=user)
            self.redirect('/post/%s' % post_id)

        except Exception, e:
            self.render('newpost.html', 
                        post={'caption' : caption, 'blobKey' : blobKey},
                        user=self.user,
                        error=e)

class Logout(BaseHandler):
    """
    Log out a user
    """

    def get(self):
        """
        Log out the user and redirect her to homepage
        """
        
        self.set_secure_cookie('user', '')
        self.redirect('/')


