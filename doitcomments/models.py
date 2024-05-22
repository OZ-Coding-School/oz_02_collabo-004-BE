from django.db import models
from users.models import User
from challenge_spoilers.models import ChallengeSpoiler

class DoItComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge_spoiler = models.ForeignKey(ChallengeSpoiler, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)