from django.urls import path
from .import views
urlpatterns =[
    path('',views.index,name='home'),
    path('login',views.log_in,name='login'),
    path('signup',views.sign_up,name='signup'),
    path('all_blogs',views.all_blogs,name='all_blogs'),
    path('blog_details',views.blog_de,name='blog_details'),
    path('logout',views.log_out,name='logout'),
    path("generate-blog/", views.generate_blog, name="generate_blog"),
]