# AmazonUnlimitedSearch
AmazonUnlimitedから指定したキーワードが含まれる書籍を検索するツール。

APIの制約上、検索結果は１回の取得で１０件。最大で１００件しか取得出来ないようです。
ということは、数千件の結果があったとしても１ページ１０件で最大１０ページ分の情報のみ取得できるということになります。
１００件では情報量が少ないと思うので、発行日が最新な書籍順にタブ区切りの文字列で結果を出します。
