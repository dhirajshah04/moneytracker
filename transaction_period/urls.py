from django.urls import path
from transaction_period import views


app_name = 'transaction_period'

urlpatterns = [
    path('settings/', views.transaction_settings_home, name='transaction_settings_home'),
    path('period/list/', views.transaction_period_list, name='transaction_period_list'),
    path('period/add/', views.transaction_period_create, name='transaction_period_create'),
    path('period/change/', views.transaction_period_change, name='transaction_period_change'),
    path('period/edit/<int:pk>/', views.transaction_period_edit, name='transaction_period_edit'),
    path('close/transaction-period/', views.close_transaction_period, name='transaction_period_close'),
]