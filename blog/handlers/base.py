
import hmac

import webapp2

from entities import blog_entity as blog
from entities import user_entity as user
import env

secret = 'Holy shIt'


##### Global Functions

def render_str(template, **params):
   """
   return rendered text from the template and parameters
   """
   t = env.jinja_env.get_template(template)
   return t.render(params)


def make_secure_cookie(value):
   """
   encode cookie value -> 'value|hash(secret + value)'
   """
   return '%s|%s' % (value, hmac.new(secret, value).hexdigest())


def check_secure_cookie(cookie):
   """
   verify if the cookie is valid. if valid,
   return the info carried by the cookie
   """
   value = cookie.split('|')[0]
   if cookie == make_secure_cookie(value):
      return value



##### Base handler

class BaseHandler(webapp2.RequestHandler):

   def __init__(self, req, res):
      """
      check if there exists
      """
      self.initialize(req, res)
      uid = self.read_secure_cookie('user_id')

      self.user = uid and user.User.by_id(int(uid))


   def write(self, text):
      """
      same as self.response.write()
      """
      self.response.write(text)


   def render(self, template, **params):
      """
      render the view to browser
      """
      self.write(render_str(template, **params))


   def set_secure_cookie(self, name, value):
      """
      set cookie: 'name=value'
      """
      cookie = make_secure_cookie(value)

      # default: path='/', expire=None, overwrite=False
      self.response.set_cookie(name, value=cookie)


   def read_secure_cookie(self, name):
      """
      if there exists cookie with name, return its cookie info
      """
      cookie_val = self.request.cookies.get(name)
      return cookie_val and check_secure_cookie(cookie_val)


   def login(self, user):
      """
      set cookie for the current user: 'user_id = user's id in db'
      """
      self.set_secure_cookie('user_id', str(user.key().id()))


   def logout(self):
      """
      delete cookie for current user
      """
      self.response.delete_cookie('user_id')





