from django.urls import path
from .views import analysis3_view

urlpatterns = [
    path('', analysis3_view, name='analysis3'),
]
