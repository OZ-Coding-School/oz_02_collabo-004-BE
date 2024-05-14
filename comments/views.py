from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from .models import Comment
from spoilers.models import Spoiler
from .serializers import CommentSerializer
# from permissions import IsOwnerOrStaff

# Spoiler 댓글 관련 기능
class CreateComment(APIView):  #챌린지 스포일러에 댓글 생성하기 (관리자, 결제유저만 가능)
    #permission_classes = [IsOwnerOrStaff]

    def post(self, request, spoiler_id):
        try:
            spoiler = Spoiler.objects.get(pk=spoiler_id)
        except Spoiler.DoesNotExist:
            return Response({"error": "Spoiler not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 요청 데이터에 spoiler_id와 user 정보 추가하여 DoItCommentSerializer 생성
        data_with_challengespoiler_id = request.data.copy()
        data_with_challengespoiler_id['spoiler_info'] = spoiler_id
        data_with_challengespoiler_id['user'] = request.user.id  # 현재 사용자 정보를 추가
        
        serializer = CommentSerializer(data=data_with_challengespoiler_id)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)