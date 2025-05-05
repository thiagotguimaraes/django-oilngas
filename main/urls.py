from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),     # Admin UI
    path('api/', include('main.wells.urls')), # Your app's API
]
