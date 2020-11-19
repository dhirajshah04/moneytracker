from django.urls import path
from pages import views

app_name = 'pages'

urlpatterns = [
    path('dashboard/report/bar-graph/', views.bar_report_home, name='bar_report_home'),
    path('dashboard/report/income-expense/json/', views.income_expense_bar_chart, name='bar_report_chart')
]
