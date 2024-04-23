from django.urls import path
from . import views

urlpatterns = [
    path('', views.analysis4_view, name='analysis4'),
]