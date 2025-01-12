from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django_pandas.io import read_frame
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from sklearn.metrics.pairwise import cosine_similarity
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd
import requests
import random
import json
from .models import DepositProducts, DepositOptions, DepositReviews, DepositJoin, SavingProducts, SavingOptions, SavingReviews, SavingJoin
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, DepositReviewsSerializer, DepositProductsViewSerializer, DepositProductsChangeSerializer, DepositJoinSerializer, SavingProductsSerializer, SavingOptionsSerializer, SavingReviewsSerializer, SavingProductsViewSerializer, SavingProductsChangeSerializer, SavingJoinSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
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
    return Response({'message': 'okay'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def list_deposits(request):
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
        if request.user.financial_products is None:
            request.user.financial_products = {}
        if deposit.fin_prdt_cd in request.user.financial_products.keys():
            DepositJoin.objects.filter(user=request.user, product=deposit).delete()
            deposit.user.remove(request.user)
            del request.user.financial_products[deposit.fin_prdt_cd]
            request.user.save()
            return Response({'message': '가입이 취소되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            option_id = request.data.get('option_id')
            selected_option = deposit.depositoptions_set.filter(id=option_id).first()
            month = selected_option.save_trm
            current_date = datetime.now().date()
            expiration_date = current_date + relativedelta(months=int(month))
            serializer = DepositJoinSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(product=deposit, user=request.user, expiration_date=expiration_date)
            deposit_info = DepositProductsViewSerializer(deposit).data
            deposit_info['depositoptions_set'] = DepositOptionsSerializer(selected_option).data
            request.user.financial_products[deposit.fin_prdt_cd] = deposit_info
            deposit.user.add(request.user)
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def change_deposits(request, fin_prdt_cd):
    deposit = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositProductsChangeSerializer(deposit, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        depositoptions_data = json.loads(list(request.data.keys())[0]).get('depositoptions_set')
        print(depositoptions_data)
        if depositoptions_data:
            for option_data in depositoptions_data:
                option_id = option_data.get('id')
                intr_rate = option_data.get('intr_rate')
                intr_rate2 = option_data.get('intr_rate2')
                if option_id:
                    if intr_rate is not None:
                        DepositOptions.objects.filter(id=option_id).update(intr_rate=intr_rate)
                    if intr_rate2 is not None:
                        DepositOptions.objects.filter(id=option_id).update(intr_rate2=intr_rate2)
        
        product_name = serializer.data['fin_prdt_nm']
        options = DepositOptions.objects.filter(product=deposit)
        if '\n' in product_name:
            product_name = product_name.replace('\n', '')
        subject = f"금리 수정 확인 - 상품명: {product_name}"
        to = list(deposit.user.values_list('email', flat=True))
        from_email = "jeho1129@naver.com"
        message = f"{product_name} 상품의 금리가 다음과 같이 변경되었습니다! \n"
        for option in options:
            save_trm = option.save_trm
            intr_rate = option.intr_rate
            intr_rate2 = option.intr_rate2
            message += f"가입 기간: {save_trm} - 금리: {intr_rate} / 우대금리: {intr_rate2} \n"
        EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        if request.user == comment.user:
            serializer = DepositReviewsSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'DELETE':
        if request.user == comment.user or request.user.is_staff:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET'])
@permission_classes([IsAdminUser])
def save_savings(request):
    API_KEY = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
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
    return Response({'message': 'okay'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def list_savings(request):
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
        if request.user.financial_products is None:
            request.user.financial_products = {}
        if saving.fin_prdt_cd in request.user.financial_products.keys():
            SavingJoin.objects.filter(user=request.user, product=saving).delete()
            saving.user.remove(request.user)
            del request.user.financial_products[saving.fin_prdt_cd]
            request.user.save()
            return Response({'message': '가입이 취소되었습니다.'}, status=status.HTTP_200_OK)
        else:
            option_id = request.data.get('option_id')
            selected_option = saving.savingoptions_set.filter(id=option_id).first()
            month = selected_option.save_trm
            current_date = datetime.now().date()
            expiration_date = current_date + relativedelta(months=int(month))
            serializer = SavingJoinSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(product=saving, user=request.user, expiration_date=expiration_date)
            saving_info = SavingProductsViewSerializer(saving).data
            saving_info['savingoptions_set'] = SavingOptionsSerializer(selected_option).data
            request.user.financial_products[saving.fin_prdt_cd] = saving_info
            saving.user.add(request.user)
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def change_savings(request, fin_prdt_cd):
    saving = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    serializer = SavingProductsChangeSerializer(saving, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        savingoptions_data =json.loads(list(request.data.keys())[0]).get('savingoptions_set')
        if savingoptions_data:
            for option_data in savingoptions_data:
                option_id = option_data.get('id')
                intr_rate = option_data.get('intr_rate')
                intr_rate2 = option_data.get('intr_rate2')
                if option_id:
                    if intr_rate is not None:
                        SavingOptions.objects.filter(id=option_id).update(intr_rate=intr_rate)
                    if intr_rate2 is not None:
                        SavingOptions.objects.filter(id=option_id).update(intr_rate2=intr_rate2)
        
        product_name = serializer.data['fin_prdt_nm']
        options = SavingOptions.objects.filter(product=saving)
        if '\n' in product_name:
            product_name = product_name.replace('\n', '')
        subject = f"금리 수정 확인 - 상품명: {product_name}"
        to = list(saving.user.values_list('email', flat=True))
        from_email = "jeho1129@naver.com"
        message = f"{product_name} 상품의 금리가 다음과 같이 변경되었습니다!\n"
        for option in options:
            save_trm = option.save_trm
            intr_rate = option.intr_rate
            intr_rate2 = option.intr_rate2
            message += f"가입 기간: {save_trm} - 금리: {intr_rate} / 우대금리: {intr_rate2}\n"
        EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        if request.user == comment.user:
            serializer = SavingReviewsSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'DELETE':
        if request.user == comment.user or request.user.is_staff:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def exchanges(request):
    API_KEY = settings.API_KEY_2
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={API_KEY}&data=AP01'
    response = requests.get(url).json()
    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def create_dummy_reviews(request):
    create_reviews(SavingProducts, SavingReviews)
    create_reviews(DepositProducts, DepositReviews)
    return Response({'message': 'Dummy reviews created successfully.'}, status=status.HTTP_201_CREATED)


def create_reviews(product_model, review_model):
    user_count = get_user_model().objects.count()
    product_count = product_model.objects.count()

    for i in range(10000):
        # 랜덤한 사용자와 상품을 선택
        random_user = get_user_model().objects.all()[random.randint(0, user_count - 1)]
        random_product = product_model.objects.all()[random.randint(0, product_count - 1)]

        # 랜덤한 평점과 내용을 생성
        random_rating = random.randint(1, 5)  # 1부터 5까지의 랜덤한 정수
        random_content = ''

        # Review 객체를 생성하고 데이터베이스에 저장
        review = review_model(product=random_product, user=random_user, rating=random_rating, content=random_content)
        review.save()


deposit_item_similarity_df = None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
    return Response(deposit_item_similarity_df.to_dict(), status=status.HTTP_201_CREATED)


# Item-Based Collaborative Filtering Algorithm
# 사용자의 행동 패턴(아이템에 대한 평점)을 분석하여, 사용자가 아직 평가하지 않은 아이템 중에 사용자가 선호할 만한 아이템을 찾아내는 방법이다.
# 아이템 간의 유사도를 계산하여, 사용자가 이미 평가한 아이템과 유사도가 높은 아이템을 추천한다.
# 사용자가 아직 아무런 아이템도 평가하지 않았거나, 모든 아이템의 유사도가 0일 경우에는 인기도가 높은 아이템을 추천하는 로직을 포함
# 새로운 사용자나 데이터가 부족한 사용자에게 추천을 제공하는 방법인 콜드 스타트 문제를 해결함.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit_recommend_items(request, user_pk, item_numbers):
    item_similarity_dict = deposit_rating_matrix(request._request).data
    item_similarity_df = deposit_item_similarity_df
    item_similarity_df = pd.DataFrame.from_dict(item_similarity_dict)
    # user_pk를 가진 사용자의 리뷰를 가져와 사용자가 평가한 상품의 ID를 리스트로 생성
    user_reviews = DepositReviews.objects.filter(user__id=user_pk)
    user_product_ids = [review.product_id for review in user_reviews]
    # item_similarity_df의 인덱스에 있는 상품 ID만을 필터링하여 유효한 상품 ID 리스트를 생성
    valid_product_ids = [product_id for product_id in user_product_ids if product_id in item_similarity_df.index]
    # user_product_ids가 DataFrame의 인덱스에 존재하는지 확인
    # 사용자가 평가한 상품이 없다면 가장 인기가 많은 아이템을 추천함.
    if not valid_product_ids:
        popular_items = item_similarity_df.sum().sort_values(ascending=False)
        recommended_items = popular_items.index[:item_numbers]
        return Response({'recommended_items': recommended_items.tolist()}, status=status.HTTP_201_CREATED)
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
    return Response({'recommended_items': recommended_items.tolist()}, status=status.HTTP_201_CREATED)


saving_item_similarity_df = None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
    return Response(saving_item_similarity_df.to_dict(), status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saving_recommend_items(request, user_pk, item_numbers):
    item_similarity_dict = saving_rating_matrix(request._request).data
    item_similarity_df = saving_item_similarity_df
    item_similarity_df = pd.DataFrame.from_dict(item_similarity_dict)
    user_reviews = SavingReviews.objects.filter(user__id=user_pk)
    user_product_ids = [review.product_id for review in user_reviews]
    valid_product_ids = [product_id for product_id in user_product_ids if product_id in item_similarity_df.index]

    if not valid_product_ids:
        popular_items = item_similarity_df.sum().sort_values(ascending=False)
        recommended_items = popular_items.index[:item_numbers]
        return Response({'recommended_items': recommended_items.tolist()}, status=status.HTTP_201_CREATED)

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

    return Response({'recommended_items': recommended_items.tolist()}, status=status.HTTP_201_CREATED)


def get_asset_group(asset):
    asset_group = asset // 1000000
    return (asset_group * 1000000, (asset_group + 1) * 1000000)


def get_salary_group(salary):
    salary_group = salary // 1000000
    return (salary_group * 1000000, (salary_group + 1) * 1000000)


def get_products(filtered_users):
    deposit_codes = set(DepositProducts.objects.values_list('fin_prdt_cd', flat=True))
    saving_codes = set(SavingProducts.objects.values_list('fin_prdt_cd', flat=True))

    deposit_products = []
    saving_products = []

    for user in filtered_users:
        if user.financial_products is not None:
            for product in user.financial_products:
                if product in deposit_codes:
                    deposit_products.append(product)
                elif product in saving_codes:
                    saving_products.append(product)

    return deposit_products, saving_products


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sorting_items(request):
    User = get_user_model()
    user = User.objects.get(pk=request.user.pk)
    
    # 나이대별 필터링
    age_filtered_users = User.objects.filter(age__range=(user.age - 5, user.age + 5))
    age_deposit_products, age_saving_products = get_products(age_filtered_users)

    # 직업 필터링
    job_filtered_users = User.objects.filter(job=user.job)
    job_deposit_products, job_saving_products = get_products(job_filtered_users)

    # 연봉 필터링
    salary_group = get_salary_group(user.salary)
    salary_filtered_users = User.objects.filter(salary__range=salary_group)
    salary_deposit_products, salary_saving_products = get_products(salary_filtered_users)

    # 자산 필터링
    asset_group = get_asset_group(user.asset)
    asset_filtered_users = User.objects.filter(asset__range=asset_group)
    asset_deposit_products, asset_saving_products = get_products(asset_filtered_users)

    result = {
    'age_deposit_products': sorted(list(set(age_deposit_products)), key=lambda x: (age_deposit_products.count(x), x), reverse=True)[:5] or ["해당 연령대의 예금 상품이 없습니다."],
    'age_saving_products': sorted(list(set(age_saving_products)), key=lambda x: (age_saving_products.count(x), x), reverse=True)[:5] or ["해당 연령대의 적금 상품이 없습니다."],
    'job_deposit_products': sorted(list(set(job_deposit_products)), key=lambda x: (job_deposit_products.count(x), x), reverse=True)[:5] or ["해당 직업군의 예금 상품이 없습니다."],
    'job_saving_products': sorted(list(set(job_saving_products)), key=lambda x: (job_saving_products.count(x), x), reverse=True)[:5] or ["해당 직업군의 적금 상품이 없습니다."],
    'salary_deposit_products': sorted(list(set(salary_deposit_products)), key=lambda x: (salary_deposit_products.count(x), x), reverse=True)[:5] or ["해당 연봉대의 예금 상품이 없습니다."],
    'salary_saving_products': sorted(list(set(salary_saving_products)), key=lambda x: (salary_saving_products.count(x), x), reverse=True)[:5] or ["해당 연봉대의 적금 상품이 없습니다."],
    'asset_deposit_products': sorted(list(set(asset_deposit_products)), key=lambda x: (asset_deposit_products.count(x), x), reverse=True)[:5] or ["해당 자산 규모의 예금 상품이 없습니다."],
    'asset_saving_products': sorted(list(set(asset_saving_products)), key=lambda x: (asset_saving_products.count(x), x), reverse=True)[:5] or ["해당 자산 규모의 적금 상품이 없습니다."],
    }

    return Response(result, status=status.HTTP_200_OK)