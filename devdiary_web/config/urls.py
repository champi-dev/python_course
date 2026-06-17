from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', obtain_auth_token, name='api_token'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('diary.api_urls')),
    path('', include('diary.urls')),
]
