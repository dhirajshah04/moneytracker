from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('pages.urls')),
    path('user/', include('users.urls')),
    path('dashboard/money/', include('money.urls')),
    path('dashboard/income-expense/', include('income_expense.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
