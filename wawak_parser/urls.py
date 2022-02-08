from django.contrib import admin
from django.urls.conf import include
from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Swagger UI
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(
        template_name="swagger-ui.html", url_name="schema"),
        name="swagger-ui",
    ),

    path('', include('checker.urls')),
]