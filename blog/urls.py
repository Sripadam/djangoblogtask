from django.contrib import admin
from django.urls import path
from blog.views import *

urlpatterns = [
    
    path("",blogs,name="blogs"),
    path("blog/<str:slug>/", blogs_comments, name="blogs_comments"),
    path("add_blogs/", AddPostView.as_view(), name="add_blogs"),
    path("edit_blog_post/<str:slug>/", UpdatePostView.as_view(), name="edit_blog_post"),
    path("delete_blog_post/<str:slug>/<int:pk>/", Delete_Blog_Post, name="delete_blog_post"),
    path("search/", search, name="search"),
    path("subscribe/",subscribe,name="subscribe"),


#user authentication
    path("register/",register,name="register"),
    path("login/",Login,name="login"),
    path("logout/",Logout,name="logout"),
    
    path("sendmail/",sendmail,name="sendmail"),
]