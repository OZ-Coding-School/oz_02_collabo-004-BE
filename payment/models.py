from django.db import models
from users.models import User
from challenges.models import ChallengeInfo
# Create your models here.
class Payment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    challenge_info=models.ForeignKey(ChallengeInfo,on_delete=models.CASCADE)
    amount = models.IntegerField(default=5000)
    merchant_uid = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    imp_uid= models.CharField(max_length=255)

    class Meta:
        db_table= 'Payment'
