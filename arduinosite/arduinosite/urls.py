from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include(('core.urls', 'core'), namespace='core')),
    path('data/', include(('data.urls', 'data'), namespace='data')),
    path('admin/', admin.site.urls),
]
