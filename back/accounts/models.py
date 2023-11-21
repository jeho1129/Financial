from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)  # 유저 ID
    name = models.CharField(max_length=30)  # 이름
    email = models.EmailField(max_length=250)  # Email
    age = models.IntegerField(blank=True, null=True)  # 나이
    asset = models.IntegerField(blank=True, null=True)  # 자산
    salary = models.IntegerField(blank=True, null=True)  # 연봉
    financial_products = models.JSONField(blank=True, null=True)  # 가입한 상품 목록
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_email, user_field, user_username

        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        name = data.get("name")
        age = data.get("age")
        asset = data.get("asset")
        salary = data.get("salary")
        financial_products = data.get("financial_products")

        user_email(user, email)
        user_username(user, username)
        user.name = name
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if age:
            user.age = age
        if asset:
            user.asset = asset
        if salary:
            user.salary = salary
        if financial_products:
            user.financial_products = financial_products
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user
