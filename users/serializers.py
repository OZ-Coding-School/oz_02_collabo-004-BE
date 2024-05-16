from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(), message='이미 존재하는 주소입니다.')])
    nickname = serializers.CharField()
    mbti = serializers.CharField()
    phone_number = serializers.CharField()
    profile_img = serializers.URLField()

    class Meta:
        model = User
        fields = ('email', 'nickname', 'mbti', 'phone_number', 'profile_img', 'is_paid', 'is_down', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(), message='이미 존재하는 주소입니다.')])

    class Meta:
        model = User
        fields = ('email', 'nickname', 'phone_number', 'profile_img')

    def create(self, validated_data):
        mbti = validated_data.pop('mbti', None)
        user = User.objects.create_user(**validated_data, mbti=mbti)
        user.save()
        return user
        
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('mbti',)
    
    def update(self, instance, validated_data):
        instance.mbti = validated_data.get('mbti', instance.mbti)
        instance.save()
        return instance