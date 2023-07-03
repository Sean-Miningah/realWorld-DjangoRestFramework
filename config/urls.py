"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse 


schema_view = get_schema_view(
    openapi.Info(
        title="Real World API",
        default_version='v1',
        description="Real World API Documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def health_view(request):
    return HttpResponse(status=200)


api_prefix = 'api'

urlpatterns = [
    path('healthz', health_view),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-redoc'),
    path(f'{api_prefix}/', include('accounts.urls')),
    path(f'{api_prefix}/', include('articles.urls')),
    path(f'{api_prefix}/', include('comments.urls'))
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL,  
                          document_root=settings.MEDIA_ROOT) 