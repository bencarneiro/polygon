"""polygon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from nft.views import get_volume, get_transactions, get_daily_sales_volume


urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_volume', get_volume, name='get_volume'),
    path('get_transactions', get_transactions, name='get_transactions'),
    path('get_daily_sales_volume', get_daily_sales_volume, name='get_daily_sales_volume')
]
