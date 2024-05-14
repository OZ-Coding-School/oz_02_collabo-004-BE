from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, nickname, mbti, phone_number, profile_img, password=None, **kwargs):
        if not email:
            raise ValueError('이메일 주소는 필수 입력 사항입니다.')
        if not nickname:
            raise ValueError('사용자는 닉네임을 갖고 있어야 합니다.')
        
        user = self.model(email=self.normalize_email(email), nickname=nickname, mbti=mbti, phone_number=phone_number, profile_img=profile_img, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nickname, mbti, phone_number, profile_img, password=None, **kwargs):
        user = self.create_user(email=email, password=password, nickname=nickname, mbti=mbti, phone_number=phone_number, profile_img=profile_img)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, verbose_name='닉네임', unique=True)
    mbti = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, verbose_name='휴대전화번호')
    profile_img = models.URLField(max_length=255)
    is_staff = models.BooleanField(default=False, verbose_name='운영진')
    is_paid = models.BooleanField(default=False, verbose_name='챌린지 도전 회원')
    is_down = models.BooleanField(default=False, verbose_name='휴면회원')
    is_active = models.BooleanField(default=True, verbose_name='활동회원')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일자')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일자')

    objects = UserManager()

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'mbti','phone_number', 'profile_img']

    LOGIN_KAKAO = 'kakao'

    login_method = models.CharField(max_length=20, default=LOGIN_KAKAO)

    def __str__(self):
        return f'{self.email} ({self.nickname})'
    
    def is_staff_member(self):
        # 사용자가 운영진인지 확인한다.
        return self.is_staff
    
    def save(self, *args, **kwargs):
        one_year_ago = timezone.now() - timezone.timedelta(days=365)
        if self.last_login and self.last_login < one_year_ago:
            self.is_down = True
            self.is_active = False

        super(User, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'users'