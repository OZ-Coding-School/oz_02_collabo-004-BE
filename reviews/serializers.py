from rest_framework import serializers
from .models import Review
from books.serializers import BookSerializer

class ReviewSerializer(serializers.ModelSerializer):

    #book = BookSerializer()
    
    class Meta:
        model = Review
        fields = "__all__"

        def create(self, validated_data):
            return Review.objects.create(**validated_data)  
