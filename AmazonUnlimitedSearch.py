#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 17:04:13 2018

@author: brokendish
"""
import bottlenose as api
import bs4
import sys
import os
import time

"""
----- AWS Key Setup -----
システムの環境変数からAWSのキーを取得するので実行するには下記の環境変数を設定する
(Bashの場合)
export AWS_ACCESS_KEY_ID=アクセスキー
export AWS_SECRET_KEY=シークレットキー
export ASSOSIATE_ID=アソシエイトID
"""
AWSAccessKeyId = os.getenv("AWS_ACCESS_KEY_ID","")
AWSSecretKey   = os.getenv("AWS_SECRET_KEY","")
AssosiateId    = os.getenv("ASSOSIATE_ID","")
# KindleUnlimitedのノードを指定
KINDLE_UMLIMITED_NODE_ID = "4486610051,2275256051"

"""
----- Amazon API -----
"""
amazon = api.Amazon(AWSAccessKeyId, AWSSecretKey, AssosiateId, Region='JP')

"""
----- unlimited_search ----------------------------------------
Amazon Kindle Unlimitedの指定したキーワードの最新１００件を表示する。
(日本国内の和書を対象にする)
制限：1時間につき3,600リクエストまで
---------------------------------------------------------------
    keywords                            :キーワード
    page                                :ページ指定※
    searchIndex="KindleStore"           :商品カテゴリ（デフォルト：KindleStore）
    browseNode=KINDLE_UMLIMITED_NODE_ID :ノードID

    ※APIの制約の制約により1度に最高で10件まで。最大件数は１００件まで
"""
def unlimited_search (keywords, page, searchIndex="KindleStore", browseNode=KINDLE_UMLIMITED_NODE_ID):
    response = amazon.ItemSearch(Keywords=keywords, SearchIndex=searchIndex, BrowseNode=browseNode, Sort="daterank",ItemPage=page,ResponseGroup="Large")
    res = bs4.BeautifulSoup(response, "lxml")
    return res


if __name__ == '__main__':
        
    keyWd=""
    keyWd=sys.argv[1]
    
    ret = unlimited_search(keyWd, 1)  
    print ("%s件見つかりましたが、100件が対象です。" % ret.find("totalresults").contents[0])   
    total_pages = ret.find("totalpages").contents[0]
    print ("ページ数: %s" % (total_pages))
    
    for pg in range(1, int(total_pages) + 1):
        print("---------- ページ: %s" % (pg))
        ret = unlimited_search(keyWd, int(pg))
        for item in ret.findAll("item"):
           detailpageurl = item.detailpageurl.contents[0] if item.detailpageurl is not None else "None" #商品ページ          
           largeimage = item.largeimage.url.contents[0] if item.largeimage is not None else "None" #商品画像（大）
           mediumimage = item.mediumimage.url.contents[0] if item.mediumimage is not None else "None" #商品画像（中）
           smallimage = item.smallimage.url.contents[0] if item.smallimage is not None else "None" #商品画像（小）
           publicationdate = item.publicationdate.contents[0] if item.publicationdate is not None else "None" #出版日
           title = item.title.contents[0] if item.title.contents[0] is not None else "None" #タイトル
           publisher = item.publisher.contents[0] if item.publisher is not None else "None" #出版社
               
           print ('{}\t{}\t{}' .format(publicationdate, title, publisher))
           #print ('{}\t{}\t{}\t{}\t{}'.format(publicationdate, title, publisher, detailpageurl, largeimage))
           
        if int(pg) == 10:
            break           
        #time.sleep(2)
        
        
    print ("----- END -----")