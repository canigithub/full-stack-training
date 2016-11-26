#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import hashlib
import hmac
import string
import random

import webapp2
import jinja2

from google.appengine.ext import db

EMPTY_EMAIL = 'Empty Email'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                autoescape=True)


###### Base handler class ######

secret = 'holy shIt'

def render_str(template, **params):
   """
   Given template and parameters, return the rendered text
   """
   t = jinja_env.get_template(template)
   return t.render(params)

def make_secure_val(val):
   """
   given a string, return the hash_str of secret+string
   """
   return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
   """
   check if the secure_val is valid via comparing the hash
   string to correct hash string
   """
   val = secure_val.split('|')[0]
   if secure_val == make_secure_val(val):
      return val

class BaseHandler(webapp2.RequestHandler):
   """
   The base handler that will be extended by other handlers
   """
   def write(self, text):
      """
      Write the response back to browser
      """
      self.response.write(text);

   def render_str(self, template, **params):
      params['user'] = self.user
      return render_str(template, **params)

   def render(self, template, **params):
      """
      Render the view use the template and parameters
      """
      self.write(render_str(template, **params))

   def set_secure_cookie(self, name, val):
      """
      set a cookie whose name is name and value is val.
      Expiration is not set
      """
      cookie_val = make_secure_val(val)
      self.response.headers.add_header(
         'Set-Cookie',
         '%s=%s; Path=/' % (name, cookie_val))

   def read_secure_cookie(self, name):
      """
      check if a cookie exists
      """
      cookie_val = self.request.cookies.get(name)
      # <=> if cookie_val and check_secure_val(cookie_val):
      #        return cookie_val
      return cookie_val and check_secure_val(cookie_val)

   def initialize(self, *a, **kw):
      """
      check for the user cookie
      """
      # check to see if user is login or not
      webapp2.RequestHandler.initialize(self, *a, **kw)
      uid = self.read_secure_cookie('user_id')
      self.user = uid and User.by_id(int(uid))


class MainPageHandler(BaseHandler):
   """
   handle '/'
   """
   def get(self):
      self.write('Hello Visiter!')


###### Blog ######

def blog_key(name='default'):
   """
   default parent key: 'blogs/default'
   """
   return db.Key.from_path('blogs', name)

class Post(db.Model):
   """
   Post object:
      subject - title of the post
      content - content of the post
      created - post created time
      last_modified - time of the most recent modify
   """
   subject = db.StringProperty(required=True)
   content = db.TextProperty(required=True)
   created = db.DateTimeProperty(auto_now_add=True)
   last_modified = db.DateTimeProperty(auto_now=True)

   def render(self):
      """
      return the html-version text of the post
      """
      self.render_content = self.content.replace('/n', '<br>')
      return render_str('post.html', p=self)


class BlogFrontHandler(BaseHandler):
   """
   handles '/blog' and display 10 most recent posts
   """
   def get(self):
      posts = db.GqlQuery("select * from Post order by created desc limit 10")
      self.render("front.html", posts=posts)


class NewPostHandler(BaseHandler):
   """
   handles '/blog/newpost'. let user submit new posts using POST method
   """
   def get(self):
      self.render("newpost.html")

   def post(self):
      subject = self.request.get("subject")
      content = self.request.get("content")

      if subject and content:
         p = Post(parent=blog_key(), subject=subject, content=content)
         p.put()
         self.redirect("/blog/%s" % str(p.key().id()))
      else:
         self.render("newpost.html", subject=subject, content=content,
                        error_msg='Please fill both subject and content!')


class PostPageHandler(BaseHandler):
   """
   handle '/blog/(\d+)', display the newly created post
   """
   def get(self, post_id):
      key = db.Key.from_path('Post', int(post_id), parent=blog_key())
      post = db.get(key)

      if not post:
         self.error(404)
         return

      self.render("permalink.html", p=post)


###### Signup ######

def hash_str(s):
   """
   use python build-in sha256 hash algorithm
   """
   return hashlib.sha256(s).hexdigest()

def make_salt():
   """
   generate a random 5 character string
   """
   return ''.join(random.SystemRandom().choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=None):
   """
   hash name, pw and salt to a string
   @return: (salt, pw_hash)
   """
   if not salt:
      salt = make_salt()
   h = hash_str(name + pw + salt)
   return '%s,%s' % (salt, h)


def user_key(group='default'):
   """
   default parent key: '/users/default'
   """
   return db.Key.from_path('users', group)

class User(db.Model):
   name = db.StringProperty(required=True)
   pw_hash = db.StringProperty(required=True)
   email = db.StringProperty()

   @classmethod
   def by_id(cls, uid):
      return User.get_by_id(uid, parent=user_key())

   @classmethod
   def by_name(cls, name):
      # <=> db.GqlQuery('select * from Users where name=name')
      return User.all().filter('name =', name).get()

   @classmethod
   def register(cls, name, pw, email=None):
      """
      create a new User object
      """
      pw_hash = make_pw_hash(name, pw)
      return User(parent=user_key(),
                  name=name,
                  pw_hash=pw_hash,
                  email=email)


def valid_pw(name, password, h):
   """
   check if password is valid
   """
   salt = h.split(',')[0]
   return h == make_pw_hash(name, pw, salt)

USER_RE = re.compile(r'^[\w-]{3,20}$')
def valid_username(username):
   return username and USER_RE.match(username)

PASSWD_RE = re.compile(r'^.{3,20}$')
def valid_password(password):
   return password and PASSWD_RE.match(password)

EMAIL_RE = re.compile(r'^\S+@\S+\.\S+$')
def valid_email(email):
   return email and EMAIL_RE.match(email)


class SignupPageHandler(BaseHandler):
   """
   handle '/blog/signup'
   """
   def get(self):
      self.render('signup-form.html')

   def post(self):

      is_error = False
      username = self.request.get('username')
      password = self.request.get('password')
      verify = self.request.get('verify')
      email = self.request.get('email')

      params = dict(username=username, email=email)

      if not valid_username(username):
         params['error_username'] = 'Not valid username'
         is_error = True

      if not valid_password(password):
         params['error_password'] = 'Not valid password'
         is_error = True
      elif password != verify:
         params['error_verify'] = 'Password not match'
         is_error = True

      if email and not valid_email(email):
         params['error_email'] = 'Not valid email'
         is_error = True

      if is_error:
         self.render('signup-form.html', **params)
      else:
         u = User.by_name(username)

         if u:
            self.render('signup-form.html',
               error_username='Username already exists')
         else:
            u = User.register(username, password, email)
            u.put()
            self.set_secure_cookie('user_id', str(u.key().id()))
            self.redirect('/welcome')


class WelcomePageHandler(BaseHandler):
   """
   handle '/blog/welcome'
   """
   def get(self):
      user_id = self.request.cookies.get('user_id').split('|')[0]

      if not user_id:
         self.write('Welcome visitor!')

      u = User.get_by_id(int(user_id), parent=user_key())
      self.write('Welcome! %s' % u.name)

###### Register routing ######

app = webapp2.WSGIApplication([
      ('/', MainPageHandler),
      ('/blog', BlogFrontHandler),
      ('/blog/newpost', NewPostHandler),
      ('/blog/(\d+)', PostPageHandler),
      ('/signup', SignupPageHandler),
      ('/welcome', WelcomePageHandler)
], debug=True)
