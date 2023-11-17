from django.urls import path
from . import views

urlpatterns = [
    path('save/deposits/', views.save_deposits),
    
]