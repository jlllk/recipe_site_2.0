from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from recipes.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.auth_urls')),
    path('user/', include('users.urls')),
    path('recipe/', include('recipes.urls')),
    path('', HomePageView.as_view(), name='home_page'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )