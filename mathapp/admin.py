from django.contrib import admin
from .models import QuestionPost,Like,Serch,Comment,Connect

# Register your models here.

class QuestionPostAdmin(admin.ModelAdmin):
    #管理ページのレコード一覧に表示するカラムを設定するクラス

    #レコードにidとtitleを表示
    list_display=("id","title")

    #表示するカラムにリンクを設定
    list_display_links=("id","title")

class LikeAdmin(admin.ModelAdmin):
    #管理ページに表示設定

    list_display=("user","question")

    list_display_links=("user","question")


class SerchAdminn(admin.ModelAdmin):
    #管理ページの表示設定

    list_display=("user","word")
    list_display_links=("user","word")


class CommentAdmin(admin.ModelAdmin):
    #管理ページの表示設定
    list_display=("user","question","comment")
    list_display_links=("user","question","comment")


class ConnectAdmin(admin.ModelAdmin):
    #フォロー管理ページの表示設定
    list_display=("user","follow")
    list_display_links=("user","follow")


#Django管理サイトにQuestionPostAdminを登録する
admin.site.register(QuestionPost,QuestionPostAdmin)

#Django管理サイトにLikeを登録
admin.site.register(Like,LikeAdmin)

#Django管理サイトにSerchを登録
admin.site.register(Serch,SerchAdminn)

#Django管理サイトにCommentを登録
admin.site.register(Comment,CommentAdmin)

#Django管理サイトにConnectを登録
admin.site.register(Connect,ConnectAdmin)