from django.db import models
from books.models import Book


class Review(models.Model):
    url = models.URLField(blank=True)
    writer = models.CharField(max_length=255,blank=True)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    type = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.title