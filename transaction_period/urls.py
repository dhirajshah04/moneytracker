from django.urls import path
from transaction_period import views


app_name = 'transaction_period'

urlpatterns = [
    path('list/', views.transaction_period_list, name='transaction_period_list'),
    path('add/', views.transaction_period_create, name='transaction_period_create'),
    path('change/', views.transaction_period_change, name='transaction_period_change'),
    path('edit/<int:pk>/', views.transaction_period_edit, name='transaction_period_edit'),
]