from django.db import models
from users.models import User
from spoilers.models import Spoiler


# Create your models here.
class Comment(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spoiler_info = models.ForeignKey(Spoiler, on_delete=models.CASCADE)
    content = models.TextField()
    is_exposed = models.BooleanField(default=False)  # -> 노출여부
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)