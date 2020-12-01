from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from recipes.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.auth_urls')),
    path('user/', include('users.urls')),
    path('recipe/', include('recipes.urls')),
    path('api/', include('api.urls')),
    path('', HomePageView.as_view(), name='home_page'),
    path(
        'about/author/',
        views.flatpage,
        {'url': '/about/author/'},
        name='about_author',
    ),
    path(
        'about/technology/',
        views.flatpage,
        {'url': '/about/technology/'},
        name='about_technology',
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )