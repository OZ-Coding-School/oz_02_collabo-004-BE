from django.db import models
from challenges.models import ChallengeInfo

class ChallengeSpoiler(models.Model):
    day = models.CharField(max_length=1)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    challenge_info = models.ForeignKey(ChallengeInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.day}일차 챌린지 스포일러 : {self.title}'