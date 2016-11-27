
from google.appengine.ext import db

import hashlib
import random
from string import letters


##### Global Functions

def hash_str(s):
   """
   genrate hash string use sha256 alg
   """
   return hashlib.sha256(s).hexdigest()


def make_salt():
   """
   generate a random 5 character string
   """
   return ''.join(random.SystemRandom().choice(letters) for x in xrange(5))


def make_passwd_hash(username, passwd, salt=None):
   """
   encode -> hash(username + passwd + salt)
   return 'salt,hash_str'
   """
   if not salt:
      salt = make_salt()
   h = hash_str(username + passwd + salt)
   return '%s,%s' % (salt, h)


def valid_pw(username, passwd, h):
   """
   check if username + passwd is valid
   """
   salt = h.split(',')[0]
   return h == make_passwd_hash(username, passwd, salt)


def user_key(group='default'):
   """
   ensure hierarchy for future use.
   default parent key: Key('users', 'default')
   """
   return db.Key.from_path('users', group)



##### Entity - User

class User(db.Model):
   """
   Entity - User:
      name - username
      pw_hash - hased password
      email - email
   """
   name = db.StringProperty(required=True)
   pw_hash = db.StringProperty(required=True)
   email = db.StringProperty()


   @classmethod
   def by_id(cls, uid):
      """
      get object using id
      """
      return User.get_by_id(uid, parent=user_key())


   @classmethod
   def by_name(cls, name):
      """
      get object using 'name' field
      """
      return User.all().filter("name = ", name).get()


   @classmethod
   def create(cls, name, passwd, email=None):
      """
      create a new User object
      """
      pw_hash = make_passwd_hash(name, passwd)
      return User(parent=user_key(),
                  name=name,
                  pw_hash=pw_hash,
                  email=email)


   @classmethod
   def login(cls, name, passwd):
      """
      check if name + passwd is valid. if valid,
      return the User object
      """
      u = cls.by_name(name)

      if u and valid_pw(name, passwd, u.pw_hash):
         return u

