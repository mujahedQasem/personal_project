from django.urls import path
from promova_app import views

urlpatterns = [
    path('',views.index),
    path('promova/login',views.login,name='login'),
    path('promova/sign-in',views.signin,name='signin'),
    path('promova/home',views.home,name='home'),
    path('promova/talk',views.talk,name='talk'),
    path('promova/images',views.images,name='images'),
    path('promova/video',views.videos,name='videos'),
    path('promova/contact-us',views.contact,name='contact'),
    path('promova/logout',views.logout,name='logout'),
   
]