from rest_framework import serializers
from .models import DepositProducts, DepositOptions, DepositReviews, SavingProducts, SavingOptions, SavingReviews
from django.contrib.auth import get_user_model

class DepositProductsSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'

    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProducts
        fields = '__all__'


class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('product',)


class DepositReviewsSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('pk', 'username')
    
    user = UserSerializer(read_only=True)

    class Meta:
        model = DepositReviews
        fields = '__all__'
        read_only_fields = ('product',)


class DepositProductsViewSerializer(serializers.ModelSerializer):
    depositreviews_set = DepositReviewsSerializer(many=True, read_only=True)
    depositreviews_count = serializers.IntegerField(source='depositreviews_set.count', read_only=True)
    
    class Meta:
        model = DepositProducts
        exclude = ('user',)

 
class SavingProductsSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'

    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = SavingProducts
        fields = '__all__'


class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('product',)


class SavingReviewsSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('pk', 'username')
    
    user = UserSerializer(read_only=True)

    class Meta:
        model = SavingReviews
        fields = '__all__'
        read_only_fields = ('product',)


class SavingProductsViewSerializer(serializers.ModelSerializer):
    savingreviews_set = SavingReviewsSerializer(many=True, read_only=True)
    savingreviews_count = serializers.IntegerField(source='savingreviews_set.count', read_only=True)
    
    class Meta:
        model = SavingProducts
        exclude = ('user',)