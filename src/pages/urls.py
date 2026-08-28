from django.urls import path

from .views import homePageView, transferView, addView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('add/', addView, name='add'),
]
