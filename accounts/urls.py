from django.urls import path
from . import views


urlpatterns = [

    path('register/', views.register, name='register'),

    path(
        'register/success/',
        views.register_success,
        name='register_success'
    ),

    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),

]