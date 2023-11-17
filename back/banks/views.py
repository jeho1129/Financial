from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .models import DepositProducts, DepositOptions, DepositReviews, SavingProducts, SavingOptions, SavingReviews
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, DepositReviewsSerializer, SavingProductsSerializer, SavingOptionsSerializer, SavingReviewsSerializer

# Create your views here.
@api_view(['GET'])
def save_deposits(request):
    API_KEY = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    for li in response.get("result").get("baseList"):
        save_data = {
            'fin_co_no' : li.get('fin_co_no'),
            'kor_co_nm' : li.get('kor_co_nm'),
            'fin_prdt_cd' : li.get('fin_prdt_cd'),
            'fin_prdt_nm' : li.get('fin_prdt_nm'),
            'join_way' : li.get('join_way'),
            'join_member' : li.get('join_member'),
            'spcl_cnd' : li.get('spcl_cnd'),
            'join_deny' : li.get('join_deny')
        }
        if not DepositProducts.objects.filter(fin_prdt_cd=save_data['fin_prdt_cd']).exists():
            serializer = DepositProductsSerializer(data=save_data, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    for li in response.get("result").get("optionList"):
        save_data = {
            'fin_prdt_cd' : li.get('fin_prdt_cd'),
            'intr_rate_type_nm' : li.get('intr_rate_type_nm'),
            'intr_rate' : li.get('intr_rate'),
            'intr_rate2' : li.get('intr_rate2'),
            'save_trm' : li.get('save_trm')
        }
        if not DepositOptions.objects.filter(fin_prdt_cd=save_data['fin_prdt_cd'], intr_rate_type_nm=save_data['intr_rate_type_nm'], intr_rate=save_data['intr_rate'], intr_rate2=save_data['intr_rate2'], save_trm=save_data['save_trm']).exists():
            product = DepositProducts.objects.get(fin_prdt_cd=save_data['fin_prdt_cd'])
            serializer = DepositOptionsSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(product=product)
    return Response({'message' : 'okay'})