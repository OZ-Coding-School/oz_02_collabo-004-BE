from django.db import models
from books.models import Book


class Review(models.Model):
    url = models.URLField(blank=True)
    writer = models.CharField(max_length=255,blank=True)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    content_type = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.title