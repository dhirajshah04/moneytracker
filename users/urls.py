from django.urls import path
from users import views


app_name = 'users'

urlpatterns = [
    path('login/', views.user_login, name='login'),
]