from django.urls import path
from income_expense import views

app_name = 'income_expense'

urlpatterns = [
    path('add-income/', views.income_add, name='income_add'),
    path('list-income/', views.income_list, name='income_list'),

    path('add-expense/', views.expense_add, name='expense_add'),
    path('list-expense/', views.expense_list, name='expense_list'),
]