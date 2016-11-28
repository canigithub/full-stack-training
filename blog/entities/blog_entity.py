
from google.appengine.ext import db

import env
import like_entity as like


##### Global Functions

def render_str(template, **params):
   """
   return rendered text from the template and parameters
   """
   t = env.jinja_env.get_template(template)
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
      user_id - the id of owner of this post
   """
   subject = db.StringProperty(required=True)
   content = db.TextProperty(required=True)
   created = db.DateTimeProperty(auto_now_add=True)
   last_modified = db.DateTimeProperty(auto_now=True)
   user_id = db.StringProperty(required=True)
   username = db.StringProperty(required=True)


   def render(self):
      """
      take current user_id of the
      return the html text of the post
      """
      self.html_content = self.content.replace('/n', '<br>')
      likes = like.Like.get_likes(str(self.key().id()))
      dislikes = like.Like.get_likes(str(self.key().id()), False)
      return render_str('post.html', p=self, likes=likes,
         dislikes=dislikes)

   @classmethod
   def by_id(cls, post_id):
      return cls.get_by_id(post_id, parent=blog_key())

   @classmethod
   def by_user_id(cls, user_id):
      # print("^^^&&&***", cls.all().filter('user_id =', user_id).count())
      # print("^^^&&&***", cls.all().filter('user_id =', user_id).get())
      return cls.all().filter('user_id =', user_id).fetch(limit=20)










