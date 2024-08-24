from django.urls import path, include
from . import views

urlpatterns = [
    path('home',views.home, name="home"),
    path('sign-up', views.sign_up, name="sign-up"),
    path('logout',views.logout, name="logout"),
    path('create-post',views.create_post, name="create-post"),

]