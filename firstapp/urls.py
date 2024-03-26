from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    
    path('home/', views.home, name = "home"),
    # path('createBlog/', views.createBlog, name ="createBlog"),
    path('blogList', views.blogList, name='blogList'),
    path('blog/<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),
    path('create_blog/', views.create_blog, name="create_blog"),
    path('blog_details/',views.blog_details,name='blog_details'),
    path('delete_blog/', views.delete_blog, name='delete_blog'),
    path('blog_list/', views.blog_list, name='blog_list'),
]
