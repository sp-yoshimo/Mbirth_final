from django.urls import path
from . import views

app_name="mathapp"

urlpatterns = [
    path("",views.NewQuestionView.as_view(),name="index"),  #新着順

    #古い投稿
    path("old/",views.OldQuestionView.as_view(),name="old"),

    #人気の投稿へのアクセス
    path("populars/",views.PopularQuestionView.as_view(),name="popular"),

    #検索ページへのアクセス
    path("serch/",views.SerchView.as_view(),name="serch"),

    #検索結果ページへのアクセス
    path("serch-result/",views.SerchView.serchresultView,name="serch_result"),

    #フォローユーザーの投稿ページへのアクセス
    path("followusers-posts/",views.FollowPostView.as_view(),name="follow_post"),

    #投稿ページのアクセス
    path("post/",views.CreateQuestionView.as_view(),name="post"),

    #詳細ページのビュー
    path("question-detail/<int:pk>",views.QuestionDetailView.detailView,name="question_detail"),

    #コメント削除へのアクセス
    path("deleted-comment/<int:pk>/<int:pk2>",views.QuestionDetailView.delete_comment_view,name="delete_comment"),

    #解答を見るページへのアクセス
    path("question-answer/<int:pk>",views.QuestionDetailView.answerView,name="question_answer"),

    #編集ページへのビュー
    path("edit-question/<int:pk>",views.question_post_updateView,name="edit"),

    #投稿削除へのアクセス
    path("delete-success/<int:pk>",views.QuestionPostDeleteView,name="delete"),

    #いいねへのアクセス
    path("like/<int:pk>",views.LikeView,name="like"),

    #ユーザーページのビュー
    path("user/<int:user>",views.UserView.as_view(),name="user_list"),

    #フォローページのビュー
    path("user-follow/<int:pk>",views.follow_view,name="follow")
]
