from django.urls import path
from . import views

urlpatterns = [
    path('deposits/save/', views.save_deposits),
    path('deposits/list/', views.list_deposits),
    path('deposits/<str:fin_prdt_cd>/', views.detail_deposits),
    path('deposits/<str:fin_prdt_cd>/comments/', views.comment_deposits),
    path('deposits/comments/<int:comment_pk>/', views.comment_deposits_detail),
    path('savings/save/', views.save_savings),
    path('savings/list/', views.list_savings),
    path('savings/<str:fin_prdt_cd>/', views.detail_savings),
    path('savings/<str:fin_prdt_cd>/comments/', views.comment_savings),
    path('savings/comments/<int:comment_pk>/', views.comment_savings_detail),
    path('exchanges/', views.exchanges),
    path('savings/recommends/dummy/', views.saving_dummy_reviews),
    path('savings/recommends/load/', views.saving_rating_matrix),
    path('savings/recommends/<int:user_pk>/<int:item_numbers>/', views.saving_recommend_items),
]