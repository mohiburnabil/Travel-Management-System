
from django import views
from django.urls import path,include
from .views import homePage,contact,about,packageList,createBlog,updateBlog,delete,loginview,logoutview,singupview,profile,packageDetails,blog_details,createpackage
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',homePage,name='homepage'),
    path('details/<str:pk>',blog_details,name = 'blog_details'),
    path('login/',loginview,name = 'login'),
    path('logout/',logoutview,name='logout'),
    path('signup/',singupview,name='signup'),
    path('profile/<str:pk>',profile,name = 'profile'),
    path('packages/',packageList,name = 'packages'),
    path('packagedetails/<str:pk>',packageDetails,name ='packagedetails' ),
    path('create blog/',createBlog,name = 'createblog'),
    path('update blog/<str:pk>/',updateBlog,name = 'updateblog'),
     path('delete/<str:pk>/',delete,name = 'delete'),
     path('createpackage/',createpackage,name = 'createpackage'),
    path('contact/',contact,name = 'contact'),
    path('about/',about,name='about')
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
