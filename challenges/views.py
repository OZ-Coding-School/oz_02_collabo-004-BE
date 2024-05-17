from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import NotFound

<<<<<<< HEAD
from .models import ChallengeInfo, ChallengeSpoiler, DoItComment
from challenges.serializers import ChallengeInfoSerializer,DoItCommentSerializer
=======
from .models import ChallengeInfo,DoItComment
from .serializers import ChallengeInfoSerializer, DoItCommentSerializer
>>>>>>> 082731488680f7da3a3ad364c2ae1ac4adf9a6e9
from books.serializers import BookSerializer
from challenge_spoilers.models import ChallengeSpoiler
from users.models import User
from books.models import Book
from payment.models import Payment
from rest_framework.decorators import api_view
#from permissions import IsOwnerOrStaff, IsPaidUserOrStaff, IsStaff

# http method  정의
    
class CreateChallenge(APIView):  # 신규챌린지 생성하기 (관리자만 가능)
    #permission_classes=[IsStaff]
    def post(self, request, book_id): 
        book = get_object_or_404(Book, pk=book_id)  # 주어진 book_id에 해당하는 Book 객체 가져오기
        request_data = request.data
        request_data['book'] = book.id

        serializer = ChallengeInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChallengeList(APIView): # 전체 챌린지 리스트 가져오기 (관리자, 로그인유저만 가능)
    #permission_classes=[IsOwnerOrStaff] #권한부여

    def get(self, request): 
        challenges = ChallengeInfo.objects.all()
        serializer = ChallengeInfoSerializer(challenges, many = True) 
        return Response(serializer.data)
    
class UpdateChallenge(APIView):  # 챌린지 정보 업데이트 하기 (관리자만 가능)
    #permission_classes=[IsStaff]

    def post(self, request, challengeinfo_id): 
        try:
            challenge_info = ChallengeInfo.objects.get(pk=challengeinfo_id)
        except ChallengeInfo.DoesNotExist:
            return Response({"message": "Challenge not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChallengeInfoSerializer(instance=challenge_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class  UserChallengeList(APIView): # 사용자가 신청한 챌린지 리스트 가져오기 (관리자, 결제유저만 가능)
    #permission_classes=[IsPaidUserOrStaff]

    def get(self, request, user_id):
        try:
            user_payments = Payment.objects.filter(user_id=user_id)
            challenge_ids = [payment.challenge_info_id for payment in user_payments]

            user_challenges = ChallengeInfo.objects.filter(id__in=challenge_ids)
            
            serializer = ChallengeInfoSerializer(user_challenges, many=True)
            
            return Response(serializer.data)
        except Payment.DoesNotExist:
            return Response({"error": "User payments not found"}, status=status.HTTP_404_NOT_FOUND)

class UserChallengeDetail(APIView): # 신청한 챌린지 상세사항 보기(관리자, 결제유저만 가능)
    #permission_classes=[IsPaidUserOrStaff] 
    def get(self, request, user_id, challengeinfo_id):
        try:
            # 사용자가 결제한 챌린지 정보를 가져옵니다.
            user_payments = Payment.objects.filter(user_id=user_id)
            challenge_ids = [payment.challenge_info_id for payment in user_payments]
            filtered_challenge = ChallengeInfo.objects.filter(id=challengeinfo_id, id__in=challenge_ids).first()

            if filtered_challenge:
                    
                    challenge_serializer = ChallengeInfoSerializer(filtered_challenge)

                    book_serializer = BookSerializer(filtered_challenge.book)

                    response_data = {
                        "challenge_info": challenge_serializer.data,
                        "book_info": book_serializer.data,
                    }

                    return Response(response_data)
            else:
                return Response({"error": "해당 챌린지 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        except Payment.DoesNotExist:
            return Response({"error": "사용자의 결제 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
class UserChallengeDo(APIView):  # 챌린지 참여현황 가져오기 - 몇 % 진행됬는지 - 구현 순서 중

    def get(self, request, user_id):
        try:
            # 해당 사용자가 신청한 모든 챌린지 가져오기
            user_payments = Payment.objects.filter(user_id=user_id)
            challenge_ids = [payment.challenge_info_id for payment in user_payments]
            user_challenges = ChallengeInfo.objects.filter(id__in=challenge_ids) #id=challengeinfo_id
            user_doing = []

            for challenge_info in user_challenges:
                total_days = 5  # 도전 챌린지 총 day 수
                challenge_spoilers = ChallengeSpoiler.objects.filter(challenge_info=challenge_info)
                completed_days = 0

                for day in range(1, total_days + 1):
                    # 해당 챌린지의 특정 일차별 스포일러 가져오기
                    try:
                        spoiler = challenge_spoilers.get(day=str(day))
                    except ChallengeSpoiler.DoesNotExist:
                        continue
                    
                    # 해당 일차별 스포일러에 달린 사용자의 댓글 수 계산
                    comment_days = DoItComment.objects.filter(challengespoiler_info=spoiler, user_id=user_id).count()
                    if comment_days > 0:
                        completed_days += 1

                # 챌린지의 완료 일수를 기반으로 사용자의 수행 백분율 계산
                doing_percentage = (completed_days / total_days) * 100

                user_doing.append({
                    'user_id': user_id,
                    'challengeinfo_id': challenge_info.id,
                    'user_doing': int(doing_percentage)  # 소수점 이하 버림
                })

            return Response(user_doing)
    
        except Payment.DoesNotExist:
                return Response({"error": "사용자의 결제 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class UserChallengeStatus(APIView):
    def get(self, request, user_id, challengeinfo_id):
        try:
            user_payments = Payment.objects.filter(user_id=user_id)
            challenge_ids = [payment.challenge_info_id for payment in user_payments]

            if int(challengeinfo_id) not in challenge_ids:
                return Response({"error": "해당 챌린지는 결제되지 않았습니다."}, status=status.HTTP_404_NOT_FOUND)

            filtered_challenge = ChallengeInfo.objects.get(id=challengeinfo_id)

            challenge_spoilers = ChallengeSpoiler.objects.filter(challenge_info=filtered_challenge)

            user_comments = DoItComment.objects.filter(user_id=user_id)

            days_status = {}
            for day in range(1, 6):  
                day_str = str(day)
                day_completed = False

                spoiler = challenge_spoilers.filter(day=day_str).first()
            
                if spoiler:
                    if user_comments.filter(challengespoiler_info=spoiler).exists():
                        day_completed = True

                days_status[day_str] = day_completed

            response_data = {
                "user_id": user_id,
                "challenge_info_id": challengeinfo_id,
                "days_status": days_status
            }

            return Response(response_data)

        except ChallengeInfo.DoesNotExist:
            return Response({"error": "해당 챌린지 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
class TotalChallenge(APIView):
    def get(self, request):
        try:
            payments = Payment.objects.all()

            unique_challenge_ids = set()

            for payment in payments:
                challenge_id = payment.challenge_info_id
                unique_challenge_ids.add(challenge_id)

            total_challenges_count = len(unique_challenge_ids)

            return Response({"진행중인 챌린지 개수": total_challenges_count})
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# challenge용 스포일러 댓글관련
class CreateDIComment(APIView):  # 챌린지 스포일러에 댓글 생성하기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]

    def post(self, request, user_id, challengeinfo_id, challengespoiler_id):
        try:
            user = User.objects.get(pk=user_id)
            
            challenge_info = ChallengeInfo.objects.get(pk=challengeinfo_id)
            challengespoiler = ChallengeSpoiler.objects.get(pk=challengespoiler_id, challenge_info=challenge_info)

            user_payments = Payment.objects.filter(user_id=user_id)
            challenge_ids = [payment.challenge_info_id for payment in user_payments]

            if int(challengeinfo_id) not in challenge_ids:
                return Response({"error": "해당 챌린지는 결제되지 않았습니다."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except ChallengeInfo.DoesNotExist:
            return Response({"error": "ChallengeInfo not found"}, status=status.HTTP_404_NOT_FOUND)
        except ChallengeSpoiler.DoesNotExist:
            return Response({"error": "ChallengeSpoiler not found"}, status=status.HTTP_404_NOT_FOUND)

        data_with_challengespoiler_id = request.data.copy()
        data_with_challengespoiler_id['challengespoiler_info'] = challengespoiler_id
        data_with_challengespoiler_id['user'] = user.id  

        serializer = DoItCommentSerializer(data=data_with_challengespoiler_id)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChallengeSpoilerComment(APIView): #챌린지 스포일러에 전체 댓글 가져오기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]

    def get(self, request, challengespoiler_id):
        try:
            challengespoiler = ChallengeSpoiler.objects.get(pk=challengespoiler_id)
        except ChallengeSpoiler.DoesNotExist:
            return Response({"error": "ChallengeSpoiler not found"}, status=status.HTTP_404_NOT_FOUND)

        # challengespoiler_id에 연결된 DoItComment 댓글들을 가져옵니다.
        doit_comments = DoItComment.objects.filter(challengespoiler_info=challengespoiler)
        serializer = DoItCommentSerializer(doit_comments, many=True)
        return Response(serializer.data)
    
class UpdateDIComment(APIView): # 챌린지용 스포일러에 댓글 업데이트 하기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]

    def put(self, request, doitcomment_id): 
        try:
            doit_comment = DoItComment.objects.get(pk=doitcomment_id)
        except DoItComment.DoesNotExist:
            return Response({"message": "DoItComment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DoItCommentSerializer(doit_comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteDIComment(APIView): # 챌린지용 스포일러에 댓글 삭제학기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]
    
    def post(self, request, doitcomment_id): 
        doitcomment_id = request.data.get('doitcomment_id')

        if not doitcomment_id:
            return Response({"error":"사용자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            doitcomment = DoItComment.objects.get(id=doitcomment_id)
        except DoItComment.DoesNotExist:
            return Response({"message": "DoItComment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        doitcomment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)