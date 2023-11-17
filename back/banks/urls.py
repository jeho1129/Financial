from django.urls import path
from . import views

urlpatterns = [
    path('deposits/save/', views.save_deposits),
    path('deposits/list/', views.list_deposits),
]