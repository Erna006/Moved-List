"""
Главный urls.py для Django проекта
Расположение: backend/backend/urls.py
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админ-панель Django
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('movies.urls')),
]

# В режиме разработки отдаем медиа и статические файлы
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Настройка заголовков админки
admin.site.site_header = "Администрирование сайта фильмов"
admin.site.site_title = "Сайт фильмов"
admin.site.index_title = "Добро пожаловать в панель управления"