from django.db import models
from django.conf import settings

# Create your models here.
class DepositProducts(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='deposits')
    fin_co_no = models.TextField()  # 금융회사 코드
    kor_co_nm = models.TextField()  # 금융회사명
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품 코드
    fin_prdt_nm = models.TextField()  # 금융 상품명
    join_way = models.TextField()  # 가입 방법
    join_member = models.TextField()  # 가입 대상
    spcl_cnd = models.TextField()  # 우대 조건
    join_deny = models.IntegerField()  # 가입 제한


class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)  # 금융 상품
    fin_prdt_cd = models.TextField()  # 금융상품 코드
    intr_rate_type_nm = models.TextField()  # 저축 금리 유형명
    intr_rate = models.FloatField(null=True)  # 저축 금리
    intr_rate2 = models.FloatField()  # 최고 우대 금리
    save_trm = models.IntegerField()  # 저축 기간


class DepositReviews(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SavingProducts(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='savings')
    fin_co_no = models.TextField()  # 금융회사 코드
    kor_co_nm = models.TextField()  # 금융회사명
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품 코드
    fin_prdt_nm = models.TextField()  # 금융 상품명
    join_way = models.TextField()  # 가입 방법
    join_member = models.TextField()  # 가입 대상
    spcl_cnd = models.TextField()  # 우대 조건
    join_deny = models.IntegerField()  # 가입 제한


class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)  # 금융 상품
    fin_prdt_cd = models.TextField()  # 금융상품 코드
    intr_rate_type_nm = models.TextField()  # 저축 금리 유형명
    intr_rate = models.FloatField()  # 저축 금리
    intr_rate2 = models.FloatField()  # 최고 우대 금리
    save_trm = models.IntegerField()  # 저축 기간


class SavingReviews(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)