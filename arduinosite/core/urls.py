from django.urls import path

from .views import HomePageView, home_page

urlpatterns = [
    # path('', HomePageView.as_view(), name='home'),
    path('', home_page, name='home'),
]