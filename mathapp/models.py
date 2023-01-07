from django.db import models
from accounts.models import CustomUser

# Create your models here.
class QuestionPost(models.Model):
    #問題投稿のデータベース
    
    #CustomUserモデルとQuestionPostモデルを1対多の関係で結びつける
    user=models.ForeignKey(
        CustomUser,
        verbose_name="ユーザー",
        #ユーザーを削除する場合はそのユーザーの投稿データもすべて削除する
        on_delete=models.CASCADE
    )

    #title用のフィールド
    title=models.CharField(
        max_length=25,
        verbose_name="問題タイトル"
        )

    #content用のフィールド
    content=models.TextField(
        verbose_name="問題文"
    )

    #img用のフィールド
    img=models.ImageField(
        verbose_name="画像(任意)",
        blank=True, #空欄でもよい
        null=True, #nullを許容
        upload_to="photos"  #MEDIA_ROOT以下のphotosにファイルを保存
    )

    #答えのフィールド
    answer=models.CharField(
        verbose_name="答え",
        max_length=30
    )

    #解説フィールド
    explain=models.TextField(
        verbose_name="解説(任意)",
        blank=True,
        null=True,
    )

    #投稿日時のフィールド
    posted_at=models.DateTimeField(
        verbose_name="投稿日時",
        auto_now_add=True  #日時を自動追加
    )


    def __str__(self):
        #オブジェクトを文字列に変換して返す
        return self.title




class Like(models.Model):
    #いいね管理用のモデル

    #誰がいいねしたかのuserフィールド
    user=models.ForeignKey(
        CustomUser,
        verbose_name="ユーザー",
        on_delete=models.CASCADE
    )

    #どの問題にいいねしたかのquestionフィールド
    question=models.ForeignKey(
        QuestionPost,
        verbose_name="問題",
        on_delete=models.CASCADE
    )


    #投稿日時
    posted_at=models.DateTimeField(
        verbose_name="投稿日時",
        auto_now_add=True
    )




class Serch(models.Model):
    #検索用のモデル
    
    #ユーザー
    user=models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="ユーザー"
    )

    #検索ワード
    word=models.CharField(
        verbose_name="検索ワード",
        max_length=50
    )

    #検索日時
    posted_at=models.DateTimeField(auto_now_add=True,verbose_name="投稿日時")



class Comment(models.Model):
    #問題に対するコメント

    #ユーザー
    user=models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="ユーザー"
    )

    #どの問題に対するコメントか
    question=models.ForeignKey(
        QuestionPost,
        on_delete=models.CASCADE,
        verbose_name="問題"
    )

    #コメント
    comment=models.TextField(
        verbose_name="コメント"
    )


class Connect(models.Model):
    #フォロー管理

    #user
    user=models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="ユーザー"
    )

    #フォローユーザー
    follow=models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="follow",
        verbose_name="フォローユーザー"
    )

    #フォロー日時
    posted_at=models.DateTimeField(
        verbose_name="フォロー日時",
        auto_now_add=True
    )