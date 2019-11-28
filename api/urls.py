"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include

from django.urls import path
# from app.user.urls import router as user_router
urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^friends', include('app.apis.friend.urls')),
    url(r'^team', include('app.apis.team.urls')),
    url(r'^mediate/', include('app.apis.mediate.urls')),
    url(r'^users', include('app.apis.user.urls')),
    url(r'^entries', include('app.apis.entries.urls')),
    url(r'^notice', include('app.apis.notification.urls')),
    url(r'^chat', include('app.apis.chat.urls')),

    url('logs/', include('app.log.urls')),
]
