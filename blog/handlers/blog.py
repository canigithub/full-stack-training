from google.appengine.ext import db

import base
from entities import user_entity as user
from entities import blog_entity as blog
from entities import like_entity as like
from entities import comment_entity as comment
import time


##### Decorators

def check_if_valid_user(func):
   def inner(*a, **kw):
      self = a[0]
      if not self.user:
         self.redirect('/login')
      else:
         return func(*a, **kw)
   return inner


def check_if_valid_post(func):
   def inner(*a, **kw):
      self = a[0]  # a[0] is self, a[1] is post_id
      post_id = a[1]
      p = blog.Post.by_id(post_id)
      if not p:
         self.error(404)
      else:
         kw['post'] = p
         return func(*a, **kw)
   return inner


def check_if_valid_comment(func):
   def inner(*a, **kw):
      self = a[0]  # a[0]:self, a[1]:comment_id
      comment_id = a[1]
      c = comment.Comment.by_id(comment_id)
      if not c:
         self.error(404)
      else:
         kw['comment'] = c
         return func(*a, **kw)
   return inner


def check_if_valid_post_user_comment(func):
   """
   check if the post_id and user_id for new comment is valid
   """
   def inner(*a, **kw):
      self = a[0]  # a[0]: self, a[1]: post_id, a[2]: user_id
      post_id = a[1]
      user_id = a[2]
      p = blog.Post.by_id(post_id)
      u = user.User.by_id(user_id)
      if not (p and u):
         self.error(404)
      else:
         return func(*a, **kw)
   return inner



def check_if_valid_post_user_like(func):
   """
   check if the post_id and user_id for like/dislike is valid
   """
   def inner(*a, **kw):
      self = a[0]  # a[0]: self, a[2]: post_id, a[3]: user_id
      post_id = a[2]
      user_id = a[3]
      p = blog.Post.by_id(post_id)
      u = user.User.by_id(user_id)
      if not (p and u):
         self.error(404)
      else:
         return func(*a, **kw)
   return inner



##### Blog Handlers

class BlogFrontPageHandler(base.BaseHandler):
   """
   handles '/blog'
   display the main page of blog section.
   """

   def get(self):
      # posts = db.GqlQuery('select * from Post order by created desc limit 10')
      posts = blog.Post.all().order('-created').fetch(limit=20)
      if not self.user:
         self.render('/logged-out/blog-front-out.html', posts=posts)
      else:
         self.render('/logged-in/blog-front-in.html', posts=posts)


class AddNewPostPageHandler(base.BaseHandler):
   """
   handles '/blog/newpost'
   display the page to create new post.
   redirect to permalink page
   """

   @check_if_valid_user
   def get(self):
      """
      if is (signed in) user, render new post page;
      otherwise, redirect to login page
      """
      self.render('/logged-in/newpost.html')


   @check_if_valid_user
   def post(self):
      """
      if not user, redirect to blog front page
      """
      subject = self.request.get('subject')
      content = self.request.get('content')

      if subject and content:
         p = blog.Post(parent=blog.blog_key(),
                  subject=subject,
                  content=content,
                  user_id=str(self.user.key().id()))
         p.put()
         self.redirect('/blog/%s' % str(p.key().id()))
      else:
         self.render('/logged-in/newpost.html',
                     subject=subject,
                     content=content,
                     error_msg='Enter both subject and content, please!')



class PermalinkPageHandler(base.BaseHandler):
   """
   handles '/blog/(\d+)' where the number is the post id
   display the newly created post.
   """

   @check_if_valid_user
   @check_if_valid_post
   def get(self, post_id, **kw):
      self.render('/logged-in/permalink.html', p=kw['post'])



class EditPostPageHandler(base.BaseHandler):
   """
   handles '/blog/edit/(\d+)' where the number is the post id
   display the to be edited post
   """

   @check_if_valid_user
   @check_if_valid_post
   def get(self, post_id, **kw):

      post = kw['post']
      if post.user_id != str(self.user.key().id()):
         self.redirect('/invalid/1')
      else:
         self.render('/logged-in/edit-post.html', p=post)


   @check_if_valid_user
   @check_if_valid_post
   def post(self, post_id, **kw):

      post = kw['post']
      if post.user_id != str(self.user.key().id()):
         self.redirect('/invalid/1')

      subject = self.request.get('subject')
      content = self.request.get('content')

      if subject and content:
         p = kw['post']
         p.subject = subject
         p.content = content
         p.put()
         self.redirect('/blog/%s' % str(p.key().id()))
      else:
         self.render('/logged-in/newpost.html',
                     subject=subject,
                     content=content,
                     error_msg='Enter both subject and content, please!')



class DeletePostHandler(base.BaseHandler):
   """
   handles '/blog/delete/(\d+)' where the number is the post id
   delete the post of post_id
   """

   @check_if_valid_user
   @check_if_valid_post
   def get(self, post_id):
      post = kw['post']
      if post.user_id != str(self.user.key().id()):
         self.redirect('/invalid/1')
      else:
         post.delete()
         time.sleep(0.1)
         self.redirect('/blog')



class PostLikeHandler(base.BaseHandler):
   """
   handles '/blog/(like|dislike)/(\d+)/(\d+)' where the number is post_id
   and user_id of that post.
   """

   @check_if_valid_user
   @check_if_valid_post_user_like
   def get(self, up, post_id, user_id):

      if user_id == str(self.user.key().id()):
         self.redirect('/invalid/2')
      elif like.Like.check_exist(post_id, str(self.user.key().id())):
         # check the post_id and user_id of the current user
         self.redirect('/invalid/4')
      else:
         lk = True if up == 'like' else False
         like.Like.add_like(post_id, str(self.user.key().id()), lk)
         time.sleep(0.1)
         self.redirect('/blog')



class MyBlogPageHandler(base.BaseHandler):
   """
   handles '/blog/myblot'
   display all posts that is posted by me
   """

   @check_if_valid_user
   def get(self):

      posts = blog.Post.by_user_id(str(self.user.key().id()))
      self.render('/logged-in/myblog.html', posts=posts)



class NewCommentPageHandler(base.BaseHandler):
   """
   handles '/blog/newcomment/(\d+)/(\d+)', number is post_id
   display page to add new comment
   """

   @check_if_valid_user
   @check_if_valid_post_user_comment
   def get(self, post_id, user_id):

      if user_id == str(self.user.key().id()):
         self.redirect('/invalid/3')
      else:
         post = blog.Post.by_id(post_id)
         self.render('/logged-in/newcomment.html', p=post)


   @check_if_valid_user
   @check_if_valid_post_user_comment
   def post(self, post_id, user_id):
      """
      user_id - user_id of the owner of the post
      """

      if user_id == str(self.user.key().id()):
         self.redirect('/invalid/3')

      content = self.request.get('content')

      if not content:
         post = blog.Post.by_id(post_id)
         self.render('/logged-in/newcomment.html', p=post, error_msg='Please enter comment')
      else:
         comment.Comment.add_comment(post_id, str(self.user.key().id()), content)
         time.sleep(0.1)
         self.redirect('/blog')



class DeleteCommentHandler(base.BaseHandler):
   """
   handles /blog/comment/delete/(\d+)
   delete the comment of comment_id
   """

   @check_if_valid_user
   @check_if_valid_comment
   def get(self, comment_id, **kw):

      c = kw['comment']
      if c.user_id != str(self.user.key().id()):
         self.redirect('/invalid/5')
      else:
         c.delete()
         time.sleep(0.1)
         self.redirect('/blog')



class EditCommentPageHandler(base.BaseHandler):
   """
   handles /blog/comment/edit/(\d+)
   edit the comment of comment_id
   """

   @check_if_valid_user
   @check_if_valid_comment
   def get(self, comment_id, **kw):

      c = kw['comment']
      p = blog.Post.by_id(c.post_id)
      if c.user_id != str(self.user.key().id()):
         self.redirect('/invalid/5')
      else:
         self.render('/logged-in/edit-comment.html',
            p=p, content=c.content)


   @check_if_valid_user
   @check_if_valid_comment
   def post(self, comment_id, **kw):

      c = kw['comment']
      if c.user_id != str(self.user.key().id()):
         self.redirect('/invalid/5')
         return

      content = self.request.get('content')
      if not content:
         post = blog.Post.by_id(post_id)
         self.render('/logged-in/newcomment.html', p=post, error_msg='Please enter comment')
      else:
         c = kw['comment']
         c.content = content
         c.put()
         time.sleep(0.1)
         self.redirect('/blog')








