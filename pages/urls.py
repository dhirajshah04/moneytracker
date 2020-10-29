from django.urls import path
from pages import views

app_name = 'pages'

urlpatterns = [
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
]
