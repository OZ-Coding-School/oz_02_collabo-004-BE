from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book
from reviews.models import Review
from django.db import models

@receiver([post_save, post_delete], sender=Review)
def update_book_is_exposed(sender, instance, **kwargs):

    book = instance.book
    review_count = Review.objects.filter(book_id=book.id).count()
    
    # 리뷰가 3개고 각 리뷰의 필드가 모두 채워져 있으면 is_exposed를 True로 설정
    review_counts_three = review_count == 3
    all_reviews_field = all(getattr(instance, field.attname) is not '' for field in instance._meta.fields if not isinstance(field, models.AutoField)) 
    all_books_field = all(getattr(book, field.attname) is not '' for field in book._meta.fields if not isinstance(field, models.AutoField))
    
    if (review_counts_three) and (all_reviews_field) and (all_books_field):
        book.is_exposed = True
    else:
        book.is_exposed = False

    # is_exposed 필드만 업데이트하도록 save 메서드 호출
    book.save(update_fields=['is_exposed'])