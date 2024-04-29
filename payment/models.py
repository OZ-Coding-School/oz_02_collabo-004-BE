from django.db import models

# Create your models here.
class Payment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    challengeInfo=models.ForeignKey(ChallengeInfo)
    price = models.IntegerField(default=5000)
    timestamp=models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    imp_uid= models.CharField(max_length=255)