from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,CreateView
from .models import QuestionPost,Like,Serch,Comment,Connect,CustomUser
from accounts.models import Introduction
from .forms import QuestionPostForm,SerchForm,CommentForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import  login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .judge import judge
from django.contrib import messages


# Made By Yoshimo

class NewQuestionView(ListView):
    #新着順のビュー
        
    #index.htmlをレンダリング
    template_name="index.html"
    #新着順に並び替え
    queryset=QuestionPost.objects.order_by("-posted_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fillter"] = "新しい投稿"  #htmlに表示させる文字列
        context["serchview"]=False  #検索結果を表示しているか

        #全ての投稿データを取得(新着順に)
        question_all=QuestionPost.objects.order_by("-id")
        good_list=[0]  #各々の問題のいいね数を格納
        for question in question_all:
            good_num=len(Like.objects.filter(question=question))  #forで選ばれた問題オブジェクトをLikeモデルのquestionフィールドのフィルタにかけて、その問題のいいね数を取得する
            good_list.append(good_num)  #good_num変数をgood_listリストに格納
        context["good_list"]=good_list  #contextにgood_listに追加
        
        return context


class OldQuestionView(ListView):
    #新着順のビュー
        
    #index.htmlをレンダリング
    template_name="index.html"

    #新着順に並び替え
    queryset=QuestionPost.objects.order_by("posted_at")
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fillter"] = "古い投稿"  #htmlに表示させる文字列
        context["serchview"]=False  #検索結果を見ているか

        #全ての投稿データを取得(古い順に)
        question_all=QuestionPost.objects.order_by("id")  #id➡登録された順に並び替え
        good_list=[0]  #各々の問題のいいね数を格納
        for question in question_all:
            good_num=len(Like.objects.filter(question=question))  #forで選ばれた問題オブジェクトをLikeモデルのquestionフィールドのフィルタにかけて、その問題のいいね数を取得する
            good_list.append(good_num)  #good_num変数をgood_listリストに格納
        context["good_list"]=good_list  #contextにgood_listに追加
        
        return context


class PopularQuestionView(ListView):
    #人気順のビュー

    #index.htmlをレンダリング
    template_name="index.html"

    def get_queryset(self):  #人気順に並び替える
        questionlist={}   #questionlist={問題のid:いいね数}という辞書を作成
        alls=QuestionPost.objects.all()  #全ての投稿データを取得
        for questiontest in alls: #questiontest変数には1つの問題オブジェクトがループのたびに入る
            questionlist[questiontest.id]=len(Like.objects.filter(question=questiontest)) #{問題のid:いいね数}の辞書を作成 。Likeモデルに問題のフィルタをかけるとその問題に対する総いいね数を取得できる
        
        #作成した辞書をいいねが多い順に並び替える  {問題のid(key):いいね数(value)}の辞書にてvalueで並び替え
        moregood = sorted(questionlist.items(), key=lambda x:x[1],reverse=True)  #valueの並び替えはlamda式で行う
    

        #いいねが多い順に並び変わったidのみ格納するリスト（現時点では空にする）
        quesids=[]
        for moregoodtuple in moregood:   #いいねが多い順になったmoregood変数は[(問題のid,いいね数),...]で並んでいるため、forでタプルを取り出してそのタプルの[0]をリストに格納
            quesids.append(moregoodtuple[0])  #quesidsにidが格納されていく

        self.querys=[]  #問題オブジェクトを格納するリスト
        for one_id in quesids:
            query=QuestionPost.objects.get(id=one_id)  #idをもとにそのidを持つ問題オブジェクトを取得
            self.querys.append(query) #取得した問題オブジェクトをquerysに格納

        return self.querys  #クエリを返す(いいねが多い順に並び変わっている)

    def get_context_data(self, **kwargs):  #htmlで表示させたいデータを辞書型で格納
        context = super().get_context_data(**kwargs)
        context["fillter"] = "人気の投稿"  #htmlに表示させる文字列
        context["serchview"]=False  #検索結果を見ているか
        good_list=[0]  #各々の問題のいいね数を格納  問題のidは1から始まるため、リストのインデックスと合わないから事前にリストにも要素を1つ入れておく
        #全ての投稿データを取得
        question_all=self.querys

        for one_questiont in question_all:
            good_num=len(Like.objects.filter(question=one_questiont))  #forで選ばれた問題オブジェクトをLikeモデルのquestionフィールドのフィルタにかけて、その問題のいいね数を取得する
            good_list.append(good_num)  #good_num変数をgood_listリストに格納

        good_list.append(0)
        context["good_list"]=good_list  #contextにgood_listに追加

        return context
    


class SerchView(CreateView):
    #検索ページのビュー
    form_class=SerchForm
    model=Serch
    template_name="serch.html"
    success_url=reverse_lazy("mathapp:serch_result")


    def form_valid(self,form):
        #フォームのバリデーションを通過したときによばれる
        #フォームデータの登録をここで行う

        #commit=FalseにしてPOSTされたデータを取得
        postdata=form.save(commit=False)
        #投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user=self.request.user
        #投稿データをデータベースに登録
        postdata.save()
        
        #過去に検索したデータを消す
        old_serch=Serch.objects.filter(user=self.request.user).order_by("id")  #過去の検索データを取得
        old_serch.delete()  #削除

        #戻り値はスーパークラスのform_vaild()の戻り値
        return super().form_valid(form)


    def serchresultView(request):
        #検索の結果ビュー
        template_name="index.html"
        #検索ワードの取得
        data=Serch.objects.filter(user=request.user).order_by("-posted_at")  
        #ユーザーを現在ログインしているものに絞り込み、最新の順に並び替える➡検索したワードはデータベースに保存しているためuserフィールドで指定して取り出す必要がある
        
        keyword=data[0].word   #dataリストの[0]には先ほど検索したwordが入る
        
        if " " in keyword or "　" in keyword:  #検索ワードにスペースが入っている場合
            keywords=keyword.split()  #スペースで区切ってリストに格納
            print(keywords)
            #絞り込み(wordの部分一致で問題オブジェクトをquery変数に格納)
            query=QuestionPost.objects.filter(Q(title__icontains=keywords[0])|Q(content__icontains=keyword[0])|Q(title__icontains=keywords[1])|Q(content__icontains=keyword[1]))#2つの単語まで対応
        else:
            ##絞り込み(wordの部分一致で問題オブジェクトをquery変数に格納)
            query=QuestionPost.objects.filter(Q(title__icontains=keyword)|Q(content__icontains=keyword))
        
        #各々の問題のいいね数を表示させるための処理
        good_list=[0]
        for one_questiont in query:
            good_num=len(Like.objects.filter(question=one_questiont))  #forで選ばれた問題オブジェクトをLikeモデルのquestionフィールドのフィルタにかけて、その問題のいいね数を取得する
            good_list.append(good_num)  #good_num変数をgood_listリストに格納
        print(good_list)
        #ctx
        ctx={
            "object_list":query,   #検索に一致する問題オブジェクトを格納
            "keyword":keyword,  #検索したワード
            "count":len(query),  #検索に一致した問題の数
            "fillter":"検索結果",  #htmlに表示する文字列
            "serchview":True,   #検索結果を表示しているかのフラグ
            "good_list":good_list  #各々の問題のいいね数うぃ格納したリスト
        }
        return render(request,template_name,ctx)
        


class FollowPostView(ListView):
    #フォローユーザーの投稿
    template_name="index.html"

    def get_queryset(self):

        #フォローユーザーを取得
        following_users=Connect.objects.filter(user=self.request.user)

        #フォローユーザーをfilterにかけて、投稿を取得  #新着順に並び替え

        q_list=QuestionPost.objects.none() #空のqueryオブジェクトを作る
        for one_follow in following_users:  #フォローユーザーを一人ずつ抽出
            q1=QuestionPost.objects.filter(user=one_follow.follow).order_by("-posted_at") #フォローユーザー一人一人の投稿を空のq_listに入れる
            q_list=q_list|q1
            
        self.query=q_list
        return self.query
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fillter"] = "フォローユーザーの投稿"
        context["have_follow"]=True

        #全ての投稿データを取得
        question_all=self.query
        good_list=[0]  #各々の問題のいいね数を格納するリスト  #数合わせのために前もって要素を一つ入れておく

        for one_questiont in question_all:
            good_num=len(Like.objects.filter(question=one_questiont))  #forで選ばれた問題オブジェクトをLikeモデルのquestionフィールドのフィルタにかけて、その問題のいいね数を取得する
            good_list.append(good_num)  #good_num変数をgood_listリストに格納


        context["good_list"]=good_list  #contextにgood_listに追加
        return context
    
    


    


#デコレーターにより、CreateViewへのアクセスはログイン中のユーザーに限定される
@method_decorator(login_required,name="dispatch")
class CreateQuestionView(CreateView):
    #問題投稿ページのビュー
    #QuestinFormで定義されているモデルとフィールドと連携して投稿データをデータベースに登録する

    #forms.pyのQuestionPostFormをフォームクラスとして登録
    form_class=QuestionPostForm
    #レンダリングするテンプレート
    template_name="post.html"
    #フォーム登録完了後のリダイレクト先
    success_url=reverse_lazy("mathapp:index")
    def form_valid(self,form):
        #フォームのバリデーションを通過したときによばれる
        #フォームデータの登録をここで行う

        #commit=FalseにしてPOSTされたデータを取得
        postdata=form.save(commit=False)
        #投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user=self.request.user
        #投稿データをデータベースに登録
        postdata.save()
        #投稿完了のメッセージを表示
        messages.success(self.request,"投稿は正常に送信されました")
        #戻り値はスーパークラスのform_vaild()の戻り値
        return super().form_valid(form)


#デコレーターにより、詳細ページへのアクセスはログイン中のユーザーに限定される
@method_decorator(login_required,name="dispatch")
class QuestionDetailView(CreateView):
    #詳細ページのビュー
    #        is_showanswer➡答えを見たか

    @login_required#ログインしているときのみアクセス可
    def detailView(request, pk):
        #詳細ページ
        ctx = {}
        #レンダリングするテンプレート
        template_name = "question_detail.html"

        #詳細を表示する問題をidから取得
        query = get_object_or_404(QuestionPost, pk=pk)

        #現在ログインしているユーザーが過去にいいねした問題をリストに格納
        likes=Like.objects.filter(user=request.user)

        liked_list=[]
        for like in likes:   #いいねした問題のidをリストに格納
            liked_list.append(like.question.id)

        #コメント送信の処理
        form=CommentForm()
        if request.method=="POST": #投稿ボタンが押されたら
            comment=request.POST["comment"]  #commentフィールドに入力された内容を取得して
            #直近の同じ問題に同じユーザーでした投稿を取得
            near_post=Comment.objects.filter(user=request.user,question=query).order_by("-id")
            if len(near_post)==0: #エラー防止のための処理
                pass
            elif comment==near_post[0].comment: #もし送信したコメントが先ほど送信したコメントと全く同じだったら
                near_post[0].delete()  #先ほど送ったコメントを削除する


            #コメントに悪意があるかの判定
            if judge(comment):#悪意がない場合   judge➡自作の関数
                obj=Comment(user=request.user,question=query,comment=comment)  #commentモデルのオブジェクトを作る
                obj.save()  #データベースに保存
                messages.success(request,"コメントを送信しました")
            else:  #悪意がる場合
                messages.warning(request,"コメントに悪意があると判断され、送信されませんでした")

        #コメント取得処理
        comments=Comment.objects.filter(question=query).order_by("-id")  #Commentモデルのフィルターにてquestionフィールドに現在閲覧している問題を格納➡現在閲覧している問題のコメント取得

        #ctxに追加
        ctx={
            "object":query,  #表示する問題
            "liked_list":liked_list,  #いいねした数が格納されているリスト　➡これを用いて問題のいいね数を表示
            "is_showanswer":False,  #答えを表示してるか
            "form":form,  #フォーム
            "comments":comments  #コメント
            }
        return render(request, template_name, ctx)


    def delete_comment_view(request,pk,pk2):
        #コメント削除ビュー
        #削除するコメントオブジェクトを取得
        obj=get_object_or_404(Comment,pk=pk)
        obj.delete()#削除実行

        context={}
        context["fillter"] = "新しい投稿"  #htmlに表示させる文字列
        context["serchview"]=False  #検索結果を表示しているか

        #全ての投稿データを取得(新着順に)
        question_all=QuestionPost.objects.order_by("-id")
        good_list=[0]  #各々の問題のいいね数を格納
        for question in question_all:
            good_num=len(Like.objects.filter(question=question))  #forで選ばれた問題オブジェクトをLikeモデルのquestionフィールドのフィルタにかけて、その問題のいいね数を取得する
            good_list.append(good_num)  #good_num変数をgood_listリストに格納
        context["good_list"]=good_list  #contextにgood_listに追加
        context["object_list"]=question_all

        messages.success(request,"コメントを削除しました")
        
        return redirect("mathapp:question_detail",pk2)




    @login_required#ログインしているときのみアクセス可
    def answerView(request, pk):
        #答え表示ページ
        #レンダリングするテンプレート
        template_name = "question_detail.html"
        ctx = {}
        #答えを表示させる問題を取得
        query = get_object_or_404(QuestionPost, pk=pk)
        #ctxに追加
        ctx["object"] = query

        #答えを表示するかのフラグ
        ctx["is_showanswer"]=True
        #問題に対するいいね数を取得
        good_num=Like.objects.filter(question=query)
        ctx["good"]=len(good_num)


        #現在ログインしているユーザーが過去にいいねした問題をリストに格納
        likes=Like.objects.filter(user=request.user)

        liked_list=[]
        for like in likes:   #いいねした問題のidをリストに格納
            liked_list.append(like.question.id)

        #コメント送信の処理
        form=CommentForm()
        if request.method=="POST": #問題に対するコメント投稿ボタンが押されたら
            comment=request.POST["comment"]  #commentフィールドに入力された内容を取得して
            #直近の同じ問題に同じユーザーでした投稿を取得
            near_post=Comment.objects.filter(user=request.user,question=query).order_by("-id")
            if len(near_post)==0: #もしコメントが一つもされてなければ
                pass  #エラー防止のための処理
            elif comment==near_post[0].comment: #もし送信したコメントが先ほど送信したコメントと全く同じだったら
                near_post[0].delete()  #先ほど送ったコメントを削除する

            #コメントに悪意があるかの判定
            if judge(comment):#悪意がない場合   judge➡自作の関数
                obj=Comment(user=request.user,question=query,comment=comment)  #commentモデルのオブジェクトを作る
                obj.save()  #データベースに保存
                #メッセージ
                messages.success(request,"コメントを送信しました")
            else:  #悪意がる場合
                messages.success(request,"コメントに悪意があると判断され、送信されませんでした")


        #コメント取得処理
        comments=Comment.objects.filter(question=query).order_by("-id")  #Commentモデルのフィルターにてquestionフィールドに現在閲覧している問題を格納➡現在閲覧している問題のコメント取得

        ctx={
            "object":query,  #表示する問題
            "liked_list":liked_list,  #いいねした数が格納
            "is_showanswer":True, #答えを表示しているか
            "form":form,  #フォーム
            "comments":comments  #コメント
            }

        return render(request, template_name, ctx)



#Ajax追加
def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def LikeView(request,pk):
    #いいねのビュー

    if request.method=="POST": #もしいいねボタンが押されたら(POSTメソッドが送信されたら)
        now_question=get_object_or_404(QuestionPost,pk=pk)  #現在閲覧している問題
        now_user=request.user  #現在ログインしているユーザー
        liked=False  #既にいいねしているかのフラグをFalseにする
        like=Like.objects.filter(user=now_user,question=now_question)
        if like.exists():  #もし現在ログインしているアカウントで現在閲覧している問題にいいねがしてあったら
            like.delete()  #データベースから削除
        else:  #もしそうでないなら
            like.create(user=now_user,question=now_question)  #データベースに登録
            liked=True   #既にいいねしているかのフラグをTrueにする

        #現在の問題に対する総いいね数を計算
        goods=len(Like.objects.filter(question=now_question))
        #ctxに追加
        ctx={
            "question_id":now_question.id,  #問題のid
            "liked":liked,   #いいねしているかの真偽
            "count":goods  #いいねされている数
        }
    if is_ajax(request): #Ajax通信でなければ何も返さない
        return JsonResponse(ctx)



#デコレーターにより、詳細ページへのアクセスはログイン中のユーザーに限定される
@method_decorator(login_required,name="dispatch")
class UserView(ListView):
    #ユーザーの投稿ビュー

    #レンダリングするテンプレート
    template_name="userpage.html"

    def get_queryset(self):

        #userのidを取得
        self.user_id=self.kwargs["user"]
        #fillterで絞り込む
        self.user_list=QuestionPost.objects.filter(user=self.user_id).order_by("-posted_at")
        return self.user_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #表示させるユーザー名
        if len(self.user_list)==0: #もしユーザーページに投稿が一つもなければ(投稿が一つもない場合そこにたどり着けるのは自分自身だけなため)
            if self.request.user.id!=self.user_id:  #もし閲覧中のユーザーページとログインしているユーザーが異なる場合
                #なんの処理も施さない
                pass
            else:
                #自分自身を表示する処理
                view_user=self.request.user  #自分自身
                context["view_user"]=view_user  #表示させるユーザー名
                context["fillter"] = "投稿一覧"
                context["all_good"]=0 #いいねされた数を0に
                obj=Introduction.objects.filter(user=view_user).order_by("-id")  #filterで絞り込みし、order_by()で最新の一言オブジェクトを取得して
                if len(obj)==0: #もし一言が一回も設定されていないなら
                    context["introduction"]=""  #introductionを空文字で返す
                else: #そうでないなら
                    context["introduction"]=str(obj[0].introduction)  #contextに引き渡す(introductionフィールドを文字列にして)
                

                #閲覧しているユーザーがいいねしてきた問題を取得
                good_questions_test=Like.objects.filter(user=view_user).order_by("-id")
                #抽出したLIkeモデルたちから問題モデルを取得
                good_questions=[]
                for oneobj in good_questions_test:
                    good_questions.append(oneobj.question)
                context["good_questions"]=good_questions

                #フォロワー・フォロー計測処理
                follow=len(Connect.objects.filter(user=self.request.user)) #フォロー
                follower=len(Connect.objects.filter(follow=self.request.user))  #フォロワー
                context["follow"]=follow
                context["follower"]=follower

                #フォロ中ーユーザー抽出処理
                follow_users=Connect.objects.filter(user=view_user)
                context["follow_users"]=follow_users

                context["other_intro"]=Introduction.objects.all()#ユーザーの一言を格納したリスト

                return context
            
        else: #もしそうではないなら
            view_user=self.user_list[0].user  #一つ目の投稿の投稿者から表示させるユーザーを取得する
            context["view_user"]=view_user  #表示させるユーザー
            #fillterに表示させる文字列
            context["fillter"] = "投稿一覧"

            #全ての投稿データを取得  ➡　各々の問題のいいね数を表示させるための処理  フィルターにて、現在閲覧しているユーザーをフィルターにかける
            question_all=QuestionPost.objects.filter(user=view_user).order_by("-id")
            good_list=[0]  #各々の問題のいいね数を格納
            for question in question_all:
                good_num=len(Like.objects.filter(question=question))  #forで選ばれた問題オブジェクトをLikeモデルのquestionフィールドのフィルタにかけて、その問題のいいね数を取得する
                good_list.append(good_num)  #good_num変数をgood_listリストに格納
            context["good_list"]=good_list  #contextにgood_listに追加

            #ユーザーの総いいね獲得数を計算する処理
            #good_listに現在閲覧しているユーザーに対する各々の問題のいいね数が入っているためsum()でユーザーの総いいね数がだせる
            all_good=sum(good_list)
            #ctxに追加
            context["all_good"]=all_good

            #閲覧しているユーザーの自己紹介・一言を取得
            obj=Introduction.objects.filter(user=view_user).order_by("-id")  #filterで絞り込みし、order_by()で最新の一言オブジェクトを取得して
            if len(obj)==0:  #もし一言が設定されていなかったら
                context["introduction"]=""  #一言を空文字で表示
            else: #そうではないなら
                context["introduction"]=str(obj[0].introduction)  #contextに引き渡す(introductionフィールドを文字列にして)

            #閲覧しているユーザーがいいねしてきた問題を取得
            good_questions_test=Like.objects.filter(user=view_user).order_by("-id")
            #抽出したLIkeモデルたちから問題モデルを取得
            good_questions=[]
            for oneobj in good_questions_test:
                good_questions.append(oneobj.question)
            context["good_questions"]=good_questions

            #フォローしてるか判定処理
            is_follow=False  #そのユーザーをフォローしているかのフラグ
            follow=Connect.objects.filter(user=self.request.user,follow=view_user)  #フィルターにかける
            if follow.exists()==False:  #もしすでにデータベースの情報からだとフォローしたあったら
                is_follow=False
            else: #そうではないなら
                is_follow=True
            #テンプレートにフォローしているかのフラグを引き渡す
            context["is_follow"]=is_follow

            #フォロワー・フォロー計測処理
            follow=len(Connect.objects.filter(user=view_user)) #フォロワー
            follower=len(Connect.objects.filter(follow=view_user))  #フォロー
            context["follow"]=follow
            context["follower"]=follower

            #フォロ中ーユーザー抽出処理
            follow_users=Connect.objects.filter(user=view_user)
            context["follow_users"]=follow_users

            context["other_intro"]=Introduction.objects.all()#ユーザーの一言を格納したリスト

            return context
    
def follow_view(request,pk):
    #フォロー処理を行うビュー

    #閲覧しているユーザー表示
    view_user=get_object_or_404(CustomUser,pk=pk)

    #もしフォローボタン、フォロー解除ボタンがクリックされたら

    #フォローをデータベースに保存する処理
    follow_obj=Connect.objects.filter(user=request.user,follow=view_user)  #フィルターにかける
    if follow_obj.exists():  #もしすでにデータベースの情報からだとフォローしたあったら
        #フォロー解除ということなのでデータベースから削除
        follow_obj.delete()
    else: #そうではないなら
        follow_obj.create(user=request.user,follow=view_user) #データベースに保存

    return redirect("mathapp:user_list",pk)



    



def question_post_updateView(request,pk):
    #問題編集のビュー
    question=get_object_or_404(QuestionPost,pk=pk)
    form=QuestionPostForm(instance=question)
    #ctxに追加
    ctx={
        "form":form,
        "object":question
    }
    if request.method=="POST": #もし更新ボタンが押されたら
        form=QuestionPostForm(request.POST,instance=question)
        if form.is_valid():
            form.user=request.user
            form.save() #データベースに保存
            #メッセージ
            messages.success(request,"問題を更新しました")
            return redirect("mathapp:question_detail",pk)

    return render(request,"edit.html",ctx)



def QuestionPostDeleteView(request,pk):
    #投稿削除ビュー

    #削除するオブジェクトを取得
    deleteobj=get_object_or_404(QuestionPost,pk=pk)
    #削除実行
    deleteobj.delete()

    #メッセージ
    messages.success(request,"問題を削除しました")

    return redirect("mathapp:index")