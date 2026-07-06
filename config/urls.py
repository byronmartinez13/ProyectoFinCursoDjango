"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from security.views import RoleSelectLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Se sobreescribe únicamente 'login' (misma URL /accounts/login/) para
    # mostrar la selección de rol por tarjetas antes del formulario real.
    # El resto de auth (logout, password_change, password_reset...) sigue
    # viniendo de django.contrib.auth.urls sin cambios.
    path('accounts/login/', RoleSelectLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('billing.urls')),
    path('purchases/', include('purchasing.urls')),
    path('security/', include('security.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
