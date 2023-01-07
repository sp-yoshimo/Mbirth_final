from django.contrib import admin
from .models import CustomUser,Introduction

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    #管理ページのレコード一覧に表示するカラムを設定するクラス

    #レコード一覧にidとusernameを表示
    list_display=("id","username")
    #表示するカラムにリンク先を設定
    list_display_links=("id","username")


class IntroductionAdmin(admin.ModelAdmin):
    #管理ページのレコード一覧に表示するカラムを設定するクラス

    #レコード一覧にidとusernameを表示
    list_display=("user","introduction")
    #表示するカラムにリンク先を設定
    list_display_links=("user","introduction")

#Django管理サイトにCustomUser、CustomUserAdminを登録する
admin.site.register(CustomUser,CustomUserAdmin)

#Django管理サイトにIntroduction、IntroductionAdminを登録する
admin.site.register(Introduction,IntroductionAdmin)