"""
URL configuration for DigitalStore project.

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

urlpatterns = [
    path('', include('StoreFront.urls')),
    path('admin/', admin.site.urls),
    path('BackStore/', include('ProductCatalog.urls')),
    path('user/', include('UserManagement.urls')),
    path('cart/', include('ShoppingCart.urls')),
    path('payment/', include('PaymentGateway.urls')),
    path('orders/', include('OrderManagement.urls')),
    path('pay/', include('Zarinpal.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
