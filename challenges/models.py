from django.db import models
from users.models import User
from books.models import Book

# Create your models here.
class ChallengeInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # 자동으로 생성되었는지 여부
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'ChallengeInfo'
