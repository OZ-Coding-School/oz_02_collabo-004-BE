from rest_framework import serializers
from .models import Book
from keywords.serializers import KeywordSerializer

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = "__all__"
        
        def create(self, validated_data):
            return Book.objects.create(**validated_data)  


class BookKeywordsSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'keywords')
