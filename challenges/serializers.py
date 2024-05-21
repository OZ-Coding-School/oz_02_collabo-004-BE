from rest_framework import serializers
from .models import ChallengeInfo


class ChallengeInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChallengeInfo
        fields = "__all__"