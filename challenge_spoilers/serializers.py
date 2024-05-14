from rest_framework import serializers
from .models import ChallengeSpoiler

class ChallengeSpoilerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChallengeSpoiler
        fields = "__all__"