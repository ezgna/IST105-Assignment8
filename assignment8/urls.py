from django.contrib import admin
from django.urls import path
from network.views import home, leases_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('leases/', leases_view, name='leases'),
]