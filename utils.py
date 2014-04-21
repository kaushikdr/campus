import hashlib
import hmac
import re

from config import *

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
GROUP_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

def render_str(template, **params):
	"""
	Return a string rendered by a Jinja2 template
	"""

	t = JINJA_ENV.get_template(template)
	return t.render(params)

def hash_str(s):
	"""
	Return an HMAC hash of the string s using the secret
	"""

	return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
	"""
	Return a secure value for cookie
	"""

	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	"""
	Check the integrity of a secure cookie
	"""

	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val

def is_username_valid(username):
	"""
	Check if username is valid
	"""

	return username and USER_RE.match(username)

def is_password_valid(password):
	"""
	Check if password is valid
	"""

	return password and PASSWORD_RE.match(password)


def is_group_valid(group):
	"""
	Check if group name is valid
	"""

	return group and GROUP_RE.match(group)

def encrypt(password):
	"""
	Encrypt the password with SHA256
	"""

	return hashlib.sha256(password).hexdigest()

class UserError(Exception):
	pass

class ValidationError(Exception):
	pass

class InvalidCredentialsError(Exception):
	pass

class AuthenticationError(Exception):
	pass