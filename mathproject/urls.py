
from django.contrib import admin
from django.urls import path,include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #mathapp.urlsへのURLパターン
    path("",include("mathapp.urls")),

    #accountsへのURLパターン
    path("",include("accounts.urls"))
]


#urlpatternにmediaフォルダーへのURLパターンを追加➡画像を読みこめるようにするため
urlpatterns+=static(
    #MEDIA_URL="media/"
    settings.MEDIA_URL,
    #MEDIAROOTにリダイレクト
    document_root=settings.MEDIA_ROOT
)