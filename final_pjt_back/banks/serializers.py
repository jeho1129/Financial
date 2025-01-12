from rest_framework import serializers
from .models import DepositProducts, DepositOptions, DepositJoin, DepositReviews, SavingProducts, SavingOptions, SavingJoin, SavingReviews
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
    depositoptions_set = DepositOptionsSerializer(many=True, read_only=True)
    depositreviews_set = DepositReviewsSerializer(many=True, read_only=True)
    depositreviews_count = serializers.IntegerField(source='depositreviews_set.count', read_only=True)

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'

    user_set = UserSerializer(many=True, read_only=True)
    user_count = serializers.IntegerField(source='user_set.count', read_only=True)
    
    class Meta:
        model = DepositProducts
        fields = '__all__'


class DepositProductsChangeSerializer(serializers.ModelSerializer):
    depositoptions_set = DepositOptionsSerializer(many=True, read_only=True)

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'

    user_set = UserSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProducts
        fields = '__all__'
        read_only_fields = ('fin_co_no', 'kor_co_nm', 'fin_prdt_cd', 'fin_prdt_nm', 'join_way', 'join_member', 'spcl_cnd', 'join_deny')

 
class DepositJoinSerializer(serializers.ModelSerializer):
    option_id = serializers.IntegerField(write_only=True)
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'
    
    user = UserSerializer(read_only=True)

    class Meta:
        model = DepositJoin
        fields = '__all__'
        read_only_fields = ('product', 'expiration_date')

    def create(self, validated_data):
        option_id = validated_data.pop('option_id')
        option = DepositOptions.objects.filter(id=option_id).first()
        return super().create({**validated_data, 'option': option})


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
    savingoptions_set = SavingOptionsSerializer(many=True, read_only=True)
    savingreviews_set = SavingReviewsSerializer(many=True, read_only=True)
    savingreviews_count = serializers.IntegerField(source='savingreviews_set.count', read_only=True)

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'

    user_set = UserSerializer(many=True, read_only=True)
    user_count = serializers.IntegerField(source='user_set.count', read_only=True)
    
    class Meta:
        model = SavingProducts
        fields = '__all__'

    
class SavingProductsChangeSerializer(serializers.ModelSerializer):
    savingoptions_set = SavingOptionsSerializer(many=True, read_only=True)

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'
            
    user_set = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = SavingProducts
        fields = '__all__'
        read_only_fields = ('fin_co_no', 'kor_co_nm', 'fin_prdt_cd', 'fin_prdt_nm', 'join_way', 'join_member', 'spcl_cnd', 'join_deny')


class SavingJoinSerializer(serializers.ModelSerializer):
    option_id = serializers.IntegerField(write_only=True)
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'
    
    user = UserSerializer(read_only=True)

    class Meta:
        model = SavingJoin
        fields = '__all__'
        read_only_fields = ('product', 'expiration_date')

    def create(self, validated_data):
        option_id = validated_data.pop('option_id')
        option = SavingOptions.objects.filter(id=option_id).first()
        return super().create({**validated_data, 'option': option})