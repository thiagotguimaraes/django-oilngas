from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import get_resolver
class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        class APIRootView(APIView):
            def get(self, request, *args, **kwargs):
                resolver = get_resolver()
                api_urls = {
                    str(pattern.pattern): request.build_absolute_uri(pattern.pattern)
                    for pattern in resolver.url_patterns
                    if pattern.pattern
                }
                return Response(api_urls)
        return APIRootView.as_view()

router = CustomRouter()

urlpatterns = [
    path('admin/', admin.site.urls), # Admin UI
    path('api/wells/', include('main.wells.urls')), # Wells API
    path('api/datasets/', include('main.datasets.urls')), # Datasets API
    path('', include(router.urls)),  # Global root API view
]
