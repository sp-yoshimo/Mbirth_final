from django.shortcuts import render,redirect
from django.views.generic import CreateView,TemplateView,FormView
from .forms import CustomUserCreationForm,ProFileForm
from .models import Introduction
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.

class SignUpView(CreateView):
    #サインアップページのビュー

    #forms.pyで定義したフォームのクラス
    form_class=CustomUserCreationForm
    #レンダリングするテンプレート
    template_name="signup.html"
    #サインアップ完了後のリダイレクト先のURLパターン
    success_url=reverse_lazy("accounts:signup_success")

    def form_valid(self,form):
        #CreateViewクラスのform_vaild()をオーバーライド

        #フォームのバリデーションを通過したときによばれる

        #formオブジェクトのフィールドの値をデータベースに保存
        user=form.save()
        self.object=user

        return super().form_valid(form)


class SignUpSuccessView(TemplateView):
    #サインアップ完了ページのビュー

    #レンダリングするテンプレート
    template_name="signup_success.html"



class ProFileView(CreateView):
    #プロフィールのビュー
    
    #レンダリングするテンプレート
    template_name="profile.html"

    #使用するFormクラス
    form_class=ProFileForm
    #送信後のリダイレクト先
    success_url=reverse_lazy("mathapp:index")
    

    def get_initial(self):  #フォームの初期値を設定
        initial = super().get_initial()
        obj=Introduction.objects.filter(user=self.request.user).order_by("-id")  #最新で設定した一言オブジェクトを取得
        if len(obj)==0: #もしまだ一言を設定していなかったら
            initial["introduction"] = ""  #空欄に一言を設定する
        else: #そうでないなら
            initial["introduction"] = obj[0].introduction  #一言オブジェクトのintroductionフィールドを初期値にする
        return initial

    def form_valid(self, form):
        #更新ボタンがクリックされたときに実行される
        data=form.save(commit=False)  #入力データを取得
        data.user=self.request.user #現在ログインしているユーザーでuserフィールドに格納
        data.save()  #データベースに登録

        old_intro=Introduction.objects.filter(user=self.request.user).order_by("id") #自分が以前に設定した一言を取得
        old_intro.delete()  #以前に設定した一言を削除

        #メッセージ
        messages.success(self.request,"プロフィールを更新しました")

        return super().form_valid(form)