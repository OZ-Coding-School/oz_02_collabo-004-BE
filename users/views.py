from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from .serializers import CreateUserSerializer, UpdateUserSerializer

# Create your views here.
User = get_user_model()

# 퍼미션 관련 커스텀으로 운영진 퍼미션 생성 및 추가
class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class UserListView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        users = User.objects.all()
        user_data = [{'id' : user.id, '닉네임': user.nickname, '계정': user.email, '연락처': user.phone_number,
                      'mbti' : user.mbti, '프로필' : user.profile_img, '운영진': user.is_staff, '챌린지': user.is_paid,
                       '휴면회원': user.is_down, '활동회원': user.is_active, '가입일': user.created_at} for user in users]
        return Response(user_data)
    
class UserDetailView(APIView):
    # 본인 확인 로직 추가
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user != user and not request.user.is_staff: # 본인 및 운영진만 조회가능
            return Response({'message':'본인의 정보만 확인할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)
        user_data = {
            'id' : user.id, '계정' : user.email, '닉네임' : user.nickname, 'mbti' : user.mbti,
            '연락처' : user.phone_number, '프로필' : user.profile_img,
            '운영진' : user.is_staff, '챌린지' : user.is_paid, '휴면회원' : user.is_down, '활동회원': user.is_active,
            '가입일' : user.created_at, '변동일' : user.updated_at, '로그인' : user.login_method
        }
        return Response(user_data)

class MyInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            'id' : user.id, '계정' : user.email, '닉네임' : user.nickname, 'mbti' : user.mbti,
            '연락처' : user.phone_number, '프로필' : user.profile_img,
            '운영진' : user.is_staff, '챌린지' : user.is_paid, '휴면회원' : user.is_down,
            '가입일자' : user.created_at, '수정일자' : user.updated_at, '로그인' : user.login_method
        }
        # 챌린지 정보 요청
        # challenge_response = requests.get('챌린지api주소')
        # if challenge_response.status_code == 200:
        #     user_data['challenge_info'] = challenge_response.json()

        # # 스포일러 정보 요청
        # spoiler_response = requests.get('스포일러api주소')
        # if spoiler_response.status_code == 200:
        #     user_data['spoiler_info'] = spoiler_response.json()

        return Response(user_data)
    
    def put(self, request):
        user = request.user
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'잘못된 요청입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    #회원탈퇴 부분
    def post(self, request):
        action = request.data.get('action')
        if action == '회원탈퇴':
            user = request.user
            user.is_active = False
            user.save()
            return Response({'message':'회원탈퇴가 완료되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':'잘못된 요청입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
class KakaoView(APIView):
    def get(self, request):
        kakao_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'
        redirect_uri = 'http://localhost:8000/users/kakao/callback'
        client_id = '4905cf8031206127649b9eadee6047ee'

        return redirect(f'{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}')
    
# 전화번호 형식 변환 함수
def convert_phone_number_format(phone_number):
    if phone_number.startswith('+82 '):
        return '0' + phone_number.split(' ')[1].replace('-', '')        
    return phone_number

class KakaoCallBackView(APIView):
    def get(self, request):
        data = {
            'grant_type' : 'authorization_code',
            'client_id' : '4905cf8031206127649b9eadee6047ee',
            'redirection_uri' : 'http://localhost:8000/users/kakao/',
            'code' : request.GET['code'],
            'client_secret': '20AWYr2edlbpkP0Lc4JJPhzXFZNP2HmK'
        }

        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        access_token = requests.post(kakao_token_api, data=data).json()['access_token']
        
        # 카카오 토큰 정보 가져오기
        kakao_user_api = 'https://kapi.kakao.com/v2/user/me'
        header = {'Authorization':f'Bearer ${access_token}'}
        kakao_user = requests.get(kakao_user_api, headers=header).json()
        print(kakao_user) #제대로 받아오는지 테스트를 위한 프린트 요청
                
        # 카카오 계정으로 사용자 조회 또는 생성
        email = kakao_user.get('kakao_account', {}).get('email', None)
        if email:
            # 데이터베이스에서 해당 이메일을 가진 사용자 조회
            try:
                user = User.objects.get(email=email)                
            # 사용자가 존재하지 않으면 새 사용자 생성
            except User.DoesNotExist:                
                # 전화번호 형식 변환
                transform_phone_number = kakao_user.get('kakao_account', {}).get('phone_number', '')                
                phone_number = convert_phone_number_format(transform_phone_number)

                serializer = CreateUserSerializer(data={
                    'email': email, 'nickname': kakao_user['properties']['nickname'],
                    'profile_img': kakao_user['properties'].get('profile_image', ''), 'phone_number': phone_number})
                
                if serializer.is_valid():
                    user = serializer.save()
                    user.set_unusable_password()
                    user.save()
                else:
                    return Response({'message':'잘못된 요청입니다.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # 토큰 생성
            refresh = RefreshToken.for_user(user)
            response = Response({'refresh':str(refresh), 'access':str(refresh.access_token),})

            # 쿠키에 토큰 저장 (세션 쿠키로 설정)
            response.set_cookie('access_token', str(refresh.access_token), httponly=True, samesite='None', secure=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True, samesite='None', secure=True)
            return response
        
        else:
            return Response({'message':'카카오 계정 이메일이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
class KakaoLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        response = Response({'message':'로그아웃 되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response