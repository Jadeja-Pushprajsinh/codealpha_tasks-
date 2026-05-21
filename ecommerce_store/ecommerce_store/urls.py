"""
URL configuration for ecommerce_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path , include
from store.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home , name='home'),
    path('product/<int:id>/',product_detail,name='product_detail'),
    path('register/', register , name='register'),
    path('cart/', cart , name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart , name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('', include('django.contrib.auth.urls')),
]