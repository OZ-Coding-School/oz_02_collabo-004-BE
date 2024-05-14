from rest_framework import serializers
from .models import Book
from keywords.serializers import KeywordSerializer

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = "__all__"
        
        def create(self, validated_data):
            return Book.objects.create(**validated_data)  
    

    '''
    def create(self, validated_data):
        # user 정보는 요청의 사용자에서
        user = self.context['request'].user
        # validated_data에서 'user' 키를 제거
        validated_data.pop('user', None)
        # 새로운 책 객체를 생성할 때 'user' 필드를 빼고 생성
        book = Book.objects.create(**validated_data)
        # 생성된 책 객체에 사용자 정보를 추가
        book.user = user
        book.save()
        return book
    '''

class BookKeywordsSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'keywords')
