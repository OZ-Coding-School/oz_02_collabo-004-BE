from rest_framework import serializers
from .models import DoItComment



class DoItCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = DoItComment
        fields = '__all__'

    def get_user(self,obj):
        return obj.user.nickname