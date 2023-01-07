from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    #Userモデルを継承したカスタムユーザーモデル
    pass

class Introduction(models.Model):
    #自己紹介等のユーザーデータ


    user=models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="ユーザー"
    )

    introduction=models.TextField(
        verbose_name="自己紹介・一言",
        null=True,
        blank=True,  #null、空白を許容
    )