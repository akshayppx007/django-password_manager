from django.contrib import admin
from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home_page, name = 'home'),
    path('login/', v.login_page, name = 'login'),
    path('register/', v.registration_page, name ='register'),
    path('logout/', v.logged_out_page,name = 'logout'),
    path('all_pws/', v.user_pw_all, name="all-page"),
    path('add_pw/', v.user_pw_add, name="add-page"),
    path('search/', v.search, name="search-page"),
    path('edit/<str:pk>/', v.edit, name="edit"),
    path('delete/<str:pk>/', v.delete, name="delete"),
]
