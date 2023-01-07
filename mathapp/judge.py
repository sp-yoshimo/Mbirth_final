from janome.tokenizer import Tokenizer

#入力されたコメントが悪意のあるものかを形態素解析を用いて判定するモジュール

#悪口リスト
dead_list=["ごみ","くそ","しね","きもい","糞","死ね","つまら","面白く","おもん","クソ","ゴミ","つまん","ひどい","酷い","ヒドイ","最低",
            "最悪","おもしろく","さいあく","さいてい",
            ]

#良い言葉リスト ➡ 「くそ楽しい」などのコメントまで除外してしまわないように
goodword_list=["最高","楽しい","難かし","神","いい","難しかっ","楽しく","よく","良く","感動","感激","かんどう","かんげき",
                "感謝","神問","かみ","むずかし","むずかっ","むずかしかっ","さいこう","たのしい"
                ]


def judge(text):  #判定するための関数
    #text ➡ コメント欄に入れられたテキスト
    tokenizer = Tokenizer(wakati=True)
    result=tokenizer.tokenize(text)
    result_list=[]
    for tkn in result:
        result_list.append(tkn)
    print(result_list)
    #形態素解析を用いる判定処理
    for dead_word in dead_list:  #悪口リストを一つずつ抽出
        for comment_word in result_list:  #入力したコメントの分割リストから一つずつ抽出
            if comment_word==dead_word:  #もし分割したコメントに悪口が入っていたら
                
                for good_word in goodword_list:   #くそ楽しい　などのフェイクがあるかもしれないのでそれの判定
                    now_index=result_list.index(comment_word)  #現在のインデックスを取得
                    if now_index!=len(result_list)-1:   #もし今のインデックスが最後の要素でなければ
                        if result_list[now_index+1]==good_word:  #もし次のインデックスのワードが良い言葉リストにあったら  
                            print("悪意のあるコメントは見つかりませんでした")  #悪意はないと判定
                            return True

                    #逆説の処理
                    if "けど" in text or "しかし" in text or "が" in text or "思ったら" in text or "おもったら" in text: #もし逆説があったら
                        print(good_word,",",dead_word)
                        if good_word in text and dead_word in text:
                            #もし deadword けれど(逆説) good_word の場合は悪意なし判定 例；最悪な問題だと思ったが、神問題だった.
                            #ようするにdeadwordの要素数<good_wordの要素数の時
                            print("ここきた")
                            if result_list.index(dead_word) < result_list.index(good_word):
                                print("悪意のあるコメントは見つかりませんでした")  #悪意はないと判定
                                return True
                            else:
                                #悪意がある判定
                                print("悪意のあるコメントが見つかりました")
                                return False


                #悪意がある判定
                print("悪意のあるコメントが見つかりました")
                return False

                
            elif "ない"==comment_word:
                #楽しくないなどの否定形の悪意のあるコメントの判定
                now_index=result_list.index(comment_word)  #現在のインデックスを取得
                for good_word in goodword_list:  #good_word変数には楽しいなどのワードが入る
                    if result_list[now_index-1]==good_word:  #もし現在の「ない」より前のワードが楽しくなどの否定を完成させてしまうものなら
                        #悪意がある判定
                        print("悪意のあるコメントが見つかりました")
                        return False
            

    #形態素解析を用いらない判定処理
    if "なよ" in text or "出すな" in text or "だすな" in text:
        print("koko")
        #「こんな問題出すなよ」　のような周りくどい悪意にあるコメントの判定
        #しかしコメントの中に良い言葉があったら  例：こんな最高で神な問題出すなよ　➡悪意あるコメントではないと判定
        for good_word in goodword_list:  #good_word変数を作成
            if good_word in text:  #もしコメントの中に良い単語が混ざっていたら
                #悪意のあるコメントは見つかりませんでした
                print("ここきた")
                print("悪意のあるコメントは見つかりませんでした")
                return True

        #悪意がある判定
        print("悪意のあるコメントが見つかりました")
        return False

    
    #悪意のあるコメントは見つかりませんでした
    print("悪意のあるコメントは見つかりませんでした")
    return True

