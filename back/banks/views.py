from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.conf import settings
from django_pandas.io import read_frame
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import requests
import random
import lorem
from .models import DepositProducts, DepositOptions, DepositReviews, SavingProducts, SavingOptions, SavingReviews
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, DepositReviewsSerializer, DepositProductsViewSerializer, SavingProductsSerializer, SavingOptionsSerializer, SavingReviewsSerializer, SavingProductsViewSerializer


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def save_deposits(request):
    API_KEY = settings.API_KEY
    request_parameters = [('020000', 1), ('030300', 4)]  # topFinGrpNo와 pageNo를 튜플로 지정
    for topFinGrpNo, maxPageNo in request_parameters:
        for pageNo in range(1, maxPageNo + 1):
            url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
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
                    serializer = DepositProductsSerializer(data=save_data)
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
    return Response({ 'message': 'okay' }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def list_deposits(request):
    if request.method == 'GET':
        deposits = DepositProducts.objects.all()
        serializer = DepositProductsViewSerializer(deposits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def detail_deposits(request, fin_prdt_cd):
    deposit = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    if request.method == 'GET':
        serializer = DepositProductsViewSerializer(deposit)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if request.user.financial_products:
            # 이미 가입한 상품이 있으면 콤마로 구분하여 추가
            request.user.financial_products += ', ' + deposit.fin_prdt_cd
        else:
            # 가입한 상품이 없으면 그대로 추가
            request.user.financial_products = deposit.fin_prdt_cd
        request.user.save()
        return Response({'message': 'Product added successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_deposits(request, fin_prdt_cd):
    deposit = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositReviewsSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(product=deposit, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_deposits_detail(request, comment_pk):
    comment = DepositReviews.objects.get(pk=comment_pk)
    if request.method == 'PUT':
        serializer = DepositReviewsSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
@permission_classes([IsAdminUser])
def save_savings(request):
    API_KEY = settings.API_KEY
    request_parameters = [('020000', 1), ('030300', 3)]

    for topFinGrpNo, maxPageNo in request_parameters:
        for pageNo in range(1, maxPageNo + 1):
            url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo={topFinGrpNo}&pageNo={pageNo}'
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

                if not SavingProducts.objects.filter(fin_prdt_cd=save_data['fin_prdt_cd']).exists():
                    serializer = SavingProductsSerializer(data=save_data)
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

                if not SavingOptions.objects.filter(fin_prdt_cd=save_data['fin_prdt_cd'], intr_rate_type_nm=save_data['intr_rate_type_nm'], intr_rate=save_data['intr_rate'], intr_rate2=save_data['intr_rate2'], save_trm=save_data['save_trm']).exists():
                    product = SavingProducts.objects.get(fin_prdt_cd=save_data['fin_prdt_cd'])
                    serializer = SavingOptionsSerializer(data=save_data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(product=product)
    return Response({ 'message': 'okay' }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def list_savings(request):
    if request.method == 'GET':
        savings = SavingProducts.objects.all()
        serializer = SavingProductsViewSerializer(savings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def detail_savings(request, fin_prdt_cd):
    saving = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    if request.method == 'GET':
        serializer = SavingProductsViewSerializer(saving)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if request.user.financial_products:
            # 이미 가입한 상품이 있으면 콤마로 구분하여 추가
            request.user.financial_products += ', ' + saving.fin_prdt_cd
        else:
            # 가입한 상품이 없으면 그대로 추가
            request.user.financial_products = saving.fin_prdt_cd
        request.user.save()
        return Response({'message': 'Product added successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_savings(request, fin_prdt_cd):
    saving = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingReviewsSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(product=saving, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_savings_detail(request, comment_pk):
    comment = SavingReviews.objects.get(pk=comment_pk)
    if request.method == 'PUT':
        serializer = SavingReviewsSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def exchanges(request):
    API_KEY = settings.API_KEY_2
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={API_KEY}&data=AP01'
    response = requests.get(url).json()
    return Response(response)


@api_view(['GET'])
def create_dummy_reviews(request):
    create_reviews(SavingProducts, SavingReviews)
    create_reviews(DepositProducts, DepositReviews)
    return Response({'message': 'Dummy reviews created successfully.'})

def create_reviews(product_model, review_model):
    user_count = get_user_model().objects.count()
    product_count = product_model.objects.count()

    for i in range(10000):
        # 랜덤한 사용자와 상품을 선택
        random_user = get_user_model().objects.all()[random.randint(0, user_count - 1)]
        random_product = product_model.objects.all()[random.randint(0, product_count - 1)]

        # 랜덤한 평점과 내용을 생성
        random_rating = random.randint(1, 5)  # 1부터 5까지의 랜덤한 정수
        random_content = lorem.text()  # 랜덤한 텍스트

        # Review 객체를 생성하고 데이터베이스에 저장
        review = review_model(product=random_product, user=random_user, rating=random_rating, content=random_content)
        review.save()


deposit_item_similarity_df = None


@api_view(['GET'])
def deposit_rating_matrix(request):
    # 사용자와 상품에 대한 평점 행렬을 생성
    reviews = DepositReviews.objects.all()
    df = read_frame(reviews, fieldnames=['user__id', 'product__id', 'rating'])
    df = df.rename(columns={'user__id': 'user_id', 'product__id': 'product_id'})
    df = df.groupby(['user_id', 'product_id']).mean().reset_index()
    rating_matrix = df.pivot(
        index='user_id',
        columns='product_id',
        values='rating'
    )
    # 상품 간의 Cosine 유사도 계산
    # 코사인 유사도는 두 벡터 간의 코사인 각을 사용하여 측정한 유사도로, 값이 1에 가까울수록 유사도가 높다는 것을 의미
    item_similarity = cosine_similarity(rating_matrix.T.fillna(0))
    deposit_item_similarity_df = pd.DataFrame(
        item_similarity,
        index = rating_matrix.columns,
        columns = rating_matrix.columns
    )
    return Response(deposit_item_similarity_df.to_dict())

# Item-Based Collaborative Filtering Algorithm
# 사용자의 행동 패턴(아이템에 대한 평점)을 분석하여, 사용자가 아직 평가하지 않은 아이템 중에 사용자가 선호할 만한 아이템을 찾아내는 방법이다.
# 아이템 간의 유사도를 계산하여, 사용자가 이미 평가한 아이템과 유사도가 높은 아이템을 추천한다.
# 사용자가 아직 아무런 아이템도 평가하지 않았거나, 모든 아이템의 유사도가 0일 경우에는 인기도가 높은 아이템을 추천하는 로직을 포함
# 새로운 사용자나 데이터가 부족한 사용자에게 추천을 제공하는 방법인 콜드 스타트 문제를 해결함.

@api_view(['GET'])
def deposit_recommend_items(request, user_pk, item_numbers):
    item_similarity_dict = saving_rating_matrix(request._request).data
    item_similarity_df = deposit_item_similarity_df
    item_similarity_df = pd.DataFrame.from_dict(item_similarity_dict)
    # user_pk를 가진 사용자의 리뷰를 가져와 사용자가 평가한 상품의 ID를 리스트로 생성
    user_reviews = DepositReviews.objects.filter(user__id=user_pk)
    user_product_ids = [review.product_id for review in user_reviews]
    
    # user_product_ids가 DataFrame의 인덱스에 존재하는지 확인
    # 사용자가 평가한 상품이 없다면 가장 인기가 많은 아이템을 추천함.
    if not set(user_product_ids).intersection(set(item_similarity_df.index)):
        popular_items = item_similarity_df.sum().sort_values(ascending=False)
        recommended_items = popular_items.index[:item_numbers]
        return Response({'recommended_items': recommended_items.tolist()})

    # 사용자가 평가한 상품이 있다면, 해당 상품에 대한 유사도를 평균내어 사용자의 평점을 계산
    user_ratings = item_similarity_df.loc[user_product_ids].mean().dropna()
    sorted_user_ratings = user_ratings.sort_values(ascending=False)
    # 사용자가 평가한 모든 아이템의 유사도가 0인 경우에는 가장 인기 있는 아이템을 추천
    if user_ratings.sum() == 0:
        popular_items = item_similarity_df.sum().sort_values(ascending=False)
        recommended_items = popular_items.index[:item_numbers]
    # 가장 높은 평점을 받은 상품과 유사한 상품을 찾아 추천
    else:
        item_similarity_df = item_similarity_df.drop(user_product_ids, errors='ignore')
        top_item_id = sorted_user_ratings.index[0]
        similar_items = item_similarity_df[top_item_id].sort_values(ascending=False)
        recommended_items = similar_items.head(item_numbers).index
    return Response({'recommended_items': recommended_items.tolist()})


saving_item_similarity_df = None


@api_view(['GET'])
def saving_rating_matrix(request):
    reviews = SavingReviews.objects.all()
    df = read_frame(reviews, fieldnames=['user__id', 'product__id', 'rating'])
    df = df.rename(columns={'user__id': 'user_id', 'product__id': 'product_id'})
    df = df.groupby(['user_id', 'product_id']).mean().reset_index()
    rating_matrix = df.pivot(
        index='user_id',
        columns='product_id',
        values='rating'
    )
    item_similarity = cosine_similarity(rating_matrix.T.fillna(0))
    saving_item_similarity_df = pd.DataFrame(
        item_similarity,
        index = rating_matrix.columns,
        columns = rating_matrix.columns
    )
    return Response(saving_item_similarity_df.to_dict())


@api_view(['GET'])
def saving_recommend_items(request, user_pk, item_numbers):
    item_similarity_dict = saving_rating_matrix(request._request).data
    item_similarity_df = saving_item_similarity_df
    item_similarity_df = pd.DataFrame.from_dict(item_similarity_dict)
    user_reviews = SavingReviews.objects.filter(user__id=user_pk)
    user_product_ids = [review.product_id for review in user_reviews]
    
    if not set(user_product_ids).intersection(set(item_similarity_df.index)):
        popular_items = item_similarity_df.sum().sort_values(ascending=False)
        recommended_items = popular_items.index[:item_numbers]
        return Response({'recommended_items': recommended_items.tolist()})

    user_ratings = item_similarity_df.loc[user_product_ids].mean().dropna()
    sorted_user_ratings = user_ratings.sort_values(ascending=False)

    if user_ratings.sum() == 0:
        popular_items = item_similarity_df.sum().sort_values(ascending=False)
        recommended_items = popular_items.index[:item_numbers]

    else:
        item_similarity_df = item_similarity_df.drop(user_product_ids, errors='ignore')
        top_item_id = sorted_user_ratings.index[0]
        similar_items = item_similarity_df[top_item_id].sort_values(ascending=False)
        recommended_items = similar_items.head(item_numbers).index

    return Response({'recommended_items': recommended_items.tolist()})