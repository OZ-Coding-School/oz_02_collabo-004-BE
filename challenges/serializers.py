from rest_framework import serializers
from .models import ChallengeInfo,DoItComment


class ChallengeInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChallengeInfo
        fields = "__all__"

class DoItCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = DoItComment
        fields = '__all__'

    def get_user(self,obj):
        return obj.user.nickname
    
# class ChallengeSpoilerSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ChallengeSpoiler
#         fields = "__all__"