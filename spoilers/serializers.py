from rest_framework import serializers
from .models import Spoiler

class SpoilerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Spoiler
        fields = "__all__"