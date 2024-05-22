from rest_framework import serializers
from .models import Review
from books.serializers import BookSerializer

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = "__all__"

        def create(self, validated_data):
        #    return Review.objects.create(**validated_data)  
            book = validated_data.pop('book')
            review = Review.objects.create(book_id=book.id, **validated_data)
            return review
