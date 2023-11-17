from django.urls import path
from . import views

urlpatterns = [
    path('deposits/save/', views.save_deposits),
    path('deposits/list/', views.list_deposits),
    path('deposits/<str:fin_prdt_cd>/', views.detail_deposits),
    path('deposits/<str:fin_prdt_cd>/comments/', views.comment_deposits),
    path('savings/save/', views.save_savings),
    path('savings/list/', views.list_savings),
    path('savings/<str:fin_prdt_cd>/', views.detail_savings),
    path('savings/<str:fin_prdt_cd>/comments/', views.comment_savings),
]