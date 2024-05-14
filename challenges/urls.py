from django.urls import path
from .views import CreateChallenge, ChallengeList, UpdateChallenge, UserChallengeList, UserChallengeDetail, UserChallengeDo

urlpatterns = [
    # 챌린지 생성하기 # 전체 챌린지 리스트 가져오기 # 챌린지 정보 업데이트 하기  
    path("challenge/create/<int:book_id>",CreateChallenge.as_view(), name='create_challenge'),
    path("challenges", ChallengeList.as_view(), name='challenge_list'),
    path("challenge/update/<int:challengeinfo_id>", UpdateChallenge.as_view(), name='update_challenge'),

    # 사용자가 신청한 챌린지 리스트 가져오기
    path("mychallenges/<int:user_id>", UserChallengeList.as_view(), name='userchallenge_list'),
    # 신청한 챌린지 상세사항 페이지 가져오기
    path('mychallenge/detail/<int:user_id>/<int:challengeinfo_id>', UserChallengeDetail.as_view(), name='userchallenge_detail'),   
    # 사용자의 챌린지 참여현황 가져오기
    path('mychallenge/doing/<int:user_id>', UserChallengeDo.as_view(), name='userchallenge_doing'),

]