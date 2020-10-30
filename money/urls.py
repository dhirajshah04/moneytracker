from django.urls import path
from money import views


app_name = 'money'

urlpatterns = [
    path('list-account/', views.account_list, name='list_account'),
    path('add-account/', views.add_account, name='add_account'),
    path('edit-account/<int:pk>/', views.edit_account, name='edit_account'),

    path('add-money/', views.add_money, name='add_money'),
]