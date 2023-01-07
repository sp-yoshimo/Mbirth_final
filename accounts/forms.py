from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import CustomUser,Introduction

class CustomUserCreationForm(UserCreationForm):
    #サインアップのフォーム
    class Meta:
        #連携するユーザーモデルを設定
        model=CustomUser

        #フォームで使用するフィールドを設定
        fields=("username","password1","password2")

class ProFileForm(ModelForm):
    #プロフィールのフォーム

    class Meta:
        #連携するモデル
        model=Introduction
        #フォームで使用するフィールド
        fields=("introduction",)