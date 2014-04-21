import webapp2

from config import *

app = webapp2.WSGIApplication([
								('/', 'views.Home'),
								('/post/([0-9]+)/?', 'views.Permalink'),
								('/download/([0-9]+)/?', 'views.downloadVideo'),
								('/dashboard/?', 'views.Dashboard'),
								('/login/?', 'views.Login'),
								('/logout/?', 'views.Logout'),
								('/signup/?', 'views.Signup'),
								('/newpost/?', 'views.NewPost'),
								('/upload/?', 'views.UploadHandler')
							], debug=False)