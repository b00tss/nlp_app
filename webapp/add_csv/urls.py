from django.urls import path
from . import views

urlpatterns = [
    path('add_csv/', views.predict, name='add_csv'),
]
