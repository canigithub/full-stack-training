
from google.appengine.ext import db

import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                autoescape=True)



##### Global Functions

def render_str(template, **params):
   """
   return rendered text from the template and parameters
   """
   t = jinja_env.get_template(template)
   return t.render(params)


def blog_key(name='default'):
   """
   ensure hierarchy for future use.
   default parent key: Key(blogs, 'default')
   """
   return db.Key.from_path('blogs', name)



##### Entity - Post

class Post(db.Model):
   """
   Entity - Post:
      subject - title of the post
      content - content of the post
      created - post created time
      last_modified - last modify time
   """
   subject = db.StringProperty(required=True)
   content = db.TextProperty(required=True)
   created = db.DateTimeProperty(auto_now_add=True)
   last_modified = db.DateTimeProperty(auto_now=True)


   def render(self):
      """
      return the html text of the post
      """
      self.html_content = self.content.replace('/n', '<br>')
      return render_str('post.html', p=self)
