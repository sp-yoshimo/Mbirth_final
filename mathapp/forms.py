from django.forms import ModelForm
from .models import QuestionPost,Like,Serch,Comment

class QuestionPostForm(ModelForm): #問題投稿フォーム
    #問題投稿のフォーム

    class Meta:
        #ModelFormのインナークラス

        model=QuestionPost #連携するモデル
        fields=["title","content","img","answer","explain"]  #htmlで表示させるフィールド

class LikeForm(ModelForm):
    #いいねのフォーム
    class Meta:

        model=Like  #連携させるモデル
        fields=[]


class SerchForm(ModelForm):
    #検索のフォーム
    class Meta:
        model=Serch  #連携させるモデル
        fields=["word"]


class CommentForm(ModelForm):
    #コメントのフォーム
    class Meta:
        model=Comment
        fields=["comment"]