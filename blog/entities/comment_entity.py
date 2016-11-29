
from google.appengine.ext import db

import env


##### Global Functions

def render_str(template, **params):
   """
   return rendered text from the template and parameters
   """
   t = env.jinja_env.get_template(template)
   return t.render(params)


def comment_key(name='default'):
   """
   ensure hierarchy for future use.
   default parent key: Key(comment, 'default')
   """
   return db.Key.from_path('comment', name)



##### Entity - Comment

class Comment(db.Model):
   """
   Entity - Comment
      user_id - user_id
      post_id - post_id
      content - comment content
      created - post created time
      last_modified - last modify time
   """
   post_id = db.StringProperty(required=True)
   user_id = db.StringProperty(required=True)
   content = db.TextProperty(required=True)
   created = db.DateTimeProperty(auto_now_add=True)
   last_modified = db.DateTimeProperty(auto_now=True)
   username = db.StringProperty(required=True)


   def render(self):
      return render_str('comment.html', c=self)

   @classmethod
   def by_id(cls, comment_id):
      """
      get comments by comment_id
      """
      return cls.get_by_id(int(comment_id), parent=comment_key())


   @classmethod
   def by_post_id(cls, post_id):
      """
      get comments belong to post_id
      """
      return cls.all().filter('post_id =', post_id).order('-created').fetch(limit=20)


   @classmethod
   def add_comment(cls, post_id, user_id, content, username):
      """
      add a new comment from user_id to post_id
      """
      c = cls(parent=comment_key(),
               post_id=post_id,
               user_id=user_id,
               content=content,
               username=username)
      c.put()






