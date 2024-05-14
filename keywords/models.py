from django.db import models
from books.models import Book

class Keyword(models.Model):
    kw = models.CharField(max_length=255)
    book_id = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.kw