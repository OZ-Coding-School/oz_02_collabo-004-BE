from django.db import models
from user.models import User
from challengeinfo.models import ChallengeInfo
# Create your models here.
class Payment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    challengeInfo=models.ForeignKey(ChallengeInfo,on_delete=models.CASCADE)
    price = models.IntegerField(default=5000)
    timestamp=models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    imp_uid= models.CharField(max_length=255)