
from google.appengine.ext import db


##### Global Functions

def like_key(name='default'):
   """
   ensure hierarchy for future use.
   default parent key: Key(likes, 'default')
   """
   return db.Key.from_path('likes', name)



##### Entity - Like

class Like(db.Model):
   """
   Entity - Like
      user_id - user_id
      post_id - post_id
      like - like or dislike
   """
   post_id = db.StringProperty(required=True)
   user_id = db.StringProperty(required=True)
   like = db.BooleanProperty(required=True)


   @classmethod
   def get_likes(cls, post_id, like=True):
      """
      get the number of likes/dislikes of a post
      """
      return cls.all().filter('post_id =', post_id).filter('like =', like).count()

   @classmethod
   def add_like(cls, post_id, user_id, like=True):
      """
      add a new like/dislike to Like
      """
      m = cls(parent=like_key(),
               post_id=post_id,
               user_id=user_id,
               like=like)
      m.put()

   @classmethod
   def check_exist(cls, post_id, user_id):
      """
      check if a user have already like/dislike a post
      """
      n = cls.all().filter('post_id =', post_id).filter('user_id =', user_id).count()
      return n != 0








