from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    published = models.CharField(max_length=255, null=True, blank=True)
    book_img = models.URLField(null=True, blank=True)
    coupang_link = models.URLField(null=True, blank=True)
    is_exposed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name