"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from account_management.urls import get_urlpatterns
from . import views

acc_urls = get_urlpatterns({
	'login': 'connexion',
	'register': 'enregistrez',
	'set-password': 'definir-mot-de-passe',
	'reset-password': 'reinitialiser-mot-de-passe',
	'logout': 'deconnecter',
})

urlpatterns = [
	path('accounts/', include(('account_management.urls', 'account_management'), namespace='account_management')),
	path('accounts2/', include((acc_urls, 'account_management'), namespace='account_management_fr')),
	path('auth/', views.AuthView.as_view(), name='auth'),
    path('admin/', admin.site.urls),
]
