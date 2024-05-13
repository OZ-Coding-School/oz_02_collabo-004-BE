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
'''
    def update_exposure(self):
        # Book 인스턴스에 속한 Review 개수 확인
        review_count = self.review_set.count()
        
        if review_count == 3:
            # Review 인스턴스가 3개인 경우 각각의 필드가 채워져 있는지 확인
            reviews = self.review_set.all()
            reviews_fields_filled = all(
                [review.url and review.writer and review.title and review.content and review.content_type for review in reviews]
            )
            
            if reviews_fields_filled:
                # 모든 조건을 만족할 때 is_exposed를 True로 설정
                self.is_exposed = True
            else:
                self.is_exposed = False
        else:
            self.is_exposed = False

        self.save() '''