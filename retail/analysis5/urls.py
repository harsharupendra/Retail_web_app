from django.urls import path
from . import views

urlpatterns = [
    path('', views.analysis5_view, name='analysis5'),
]