#前提
    #起動は　python t.py
    #フォルダは　カレントの下にrecを用意すること
    #　その中にrec.csv、toko.log、geko.logが記録される
    #  テスト時これらのファイルは消しておくこと

import pygame
from pygame.locals import *
import datetime
import csv
import sys
import os
#from datetime import datetime
import g_aisatu
import g_input_taion
import g_kakunin
import g_message
import g_kyosi
import g_input

#モードの決定
def id2mode(id,id_list):
    if id==999:
        mode="kyosi"
        return mode
    if id>len(students):
        return "input err"
    else:
        if id in id_list:
            mode="geko"
        else:
            mode="toko"        
    return mode

def getLogData():#tokos[]　gekos[]
    #登校データ取得
    try: 
        with open('rec/toko.log', 'r', encoding='utf-8') as f:
            tokos = [r for r in csv.reader(f)]        
    except FileNotFoundError:
        with open('rec/toko.log', 'w', encoding='utf-8') as f:
            tokos = []
    #下校データ取得　　
    try:
        with open('rec/geko.log', 'r', encoding='utf-8') as f:
            gekos = [r for r in csv.reader(f)]
    except FileNotFoundError:
        with open('rec/geko.log', 'w', encoding='utf-8') as f:
            gekos = []
    return tokos,gekos

#ログデータを見て在校生徒を調べる
def make_id_list():
    tokos,gekos=getLogData()    #ログデータから登校、下校両方のデータを取得　　
    id_lists=[]
    #生徒の数ぶん、logデータを拾って統合していく、登校がなければ欠席
    #最初はidの0番から
    for id in range(len(students)):
        #1人分のデータ,idと名前
        #one=[str(id),students[id]]
        #1人分の登校データを作成、登校logの中からidを探す
        for t in tokos:
            if int(t[0]) == id:#ログの中にidがみつかったら：
                id_lists.append(id)#id_listsに追加
                break#みつかったらブレーク
        #1人分、下校logの中からidを探す
        for t in gekos:
            if int(t[0]) == id:#見つかったら
                id_lists.remove(id)# 削除９９
                break#みつかったらブレーク
    return id_lists    


def mrgs2csv(Tsets):#mrgsデータをcsvとして書き込む
    mrgs=make_mrgs(Tsets)#ログから配列データの作成
    now = datetime.datetime.now()    
    date = now.date()
    dstr=str(date)

    #書き込み
    #with open('rec/rec.csv', 'w', encoding='sjis',newline='') as f:
    with open('rec/rec.csv', 'a', encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        #writer.writerows(mrgs)
        for mrgs1 in mrgs:
            mrgs1.insert(0,dstr)
            writer.writerow(mrgs1)

    os.rename("rec/toko.log", "rec/toko"+dstr+".log")#今ある.logは日付付きに名前を変更
    os.rename("rec/geko.log", "rec/geko"+dstr+".log")

def make_mrgs(Tsets):
    """以下のような表示用のデータを作成する
    mrgs=[["id","名前","登校時","下校時","登校時刻","下校時刻","体温"]
          ['0', '江夏豊', '遅刻', '早退', '8:24', '16:24', '36.0'],
                ...
          ['9', '佐々木小次郎', '欠席', '', '', '', '']]
    """        
    tokoh=Tsets["tokoh"]
    tokom=Tsets["tokom"]
    gekoh=Tsets["gekoh"]
    gekom=Tsets["gekom"]
    tokos,gekos=getLogData()    #登校、下校データ取得　　
    #idの0番から生徒の数だけlogデータを拾って統合していく、登校がなければ欠席
    mrgs=[["id","名前","登校時","下校時","登校時刻","下校時刻","体温"]]
    for id in range(len(students)):
        P1=PersonalData()
        #1人分のデータ,idと名前
        P1.id = str(id)
        P1.name = students[id]
        #1人分の登校データを作成、登校logの中からidを探す
        isFound=False
        for toko in tokos:
            if int(toko[0])==id:#みつかったら以下
                isFound=True
                #時刻だけ抜き出す
                dt = datetime.datetime.strptime(toko[2], '%Y-%m-%d %H:%M:%S.%f')
                P1.toko_t=str(dt.hour)+":"+str(dt.minute)
                #遅刻の判定
                if dt.time() > datetime.time(tokoh, tokom):
                    P1.toko = "遅刻"
                else:
                    P1.toko = ""
                #体温追加
                P1.taion=toko[3]
                break#みつかったらブレーク
        if isFound==False:#logに登校記録がなければ欠席
            P1.toko="欠席"
        #1人分、下校logの中からidを探す
        for toko in gekos:
            if int(toko[0]) == id:#見つかったら下校時刻だけくっつける
                #時刻だけ抜き出す
                dt = datetime.datetime.strptime(toko[2], '%Y-%m-%d %H:%M:%S.%f')
                P1.geko_t=str(dt.hour)+":"+str(dt.minute)
                #早退の判定
                if dt.time() > datetime.time(gekoh, gekom):
                    P1.geko = ""
                else:
                    P1.geko = "早退" 
                break#みつかったらブレーク
        mrgs.append([P1.id,P1.name,P1.toko,P1.geko,P1.toko_t,P1.geko_t,P1.taion])
    #print("@136 mrgs=",mrgs)
    return mrgs

#教師モード
def kyosi(Gsets,Tsets):
    screen=Gsets[0]
    font=Gsets[1]
    font2=Gsets[2]
    while True:
        jb=g_kyosi.kyosi(Gsets)
        if jb==1:#データ出力
            mrgs = make_mrgs(Tsets)
            while True:
                screen.fill((200,255,200))
                xx=20
                ww=800
                yy=50
                isLoop=True
                mes="csvデータ作成:okならエンターを押してね"
                txt_g = font.render(mes, True, (55,55,55)) # 描画する文字列を画像にする
                screen.blit(txt_g, [xx, yy])                    # 画像を表示

                mes = "登校"+str(Tsets["tokoh"]) + ":" + str(Tsets["tokom"]) + "～下校" + str(Tsets["gekoh"]) + ":" + str(Tsets["gekom"])
                txt_g = font2.render(mes, True, (55,55,55)) # 描画する文字列を画像にする
                screen.blit(txt_g, [xx, yy+50])                    # 画像を表示
                yy+=50
                #ここに出欠表を書く
                pygame.draw.rect(screen, (0,155,0), Rect(xx,yy+50,ww,len(mrgs)*50), 2) # 外枠
                for i in range(len(mrgs)):
                    m1=mrgs[i]
                    yy+=50
                    pygame.draw.line(screen, (0,155,0), (xx,yy+50), (xx+ww,yy+50), 2)  # 線
                    txt_g = font2.render(m1[0], True, (0,55,0))#ID
                    screen.blit(txt_g, [xx+20, yy+10])
                    if m1[4]!="" and m1[5]=="":#校舎にいるなら              
                        txt_g = font2.render(m1[1], True, (155,0,0))#名前赤で
                    else:
                        txt_g = font2.render(m1[1], True, (0,55,0))#名前
                    screen.blit(txt_g, [xx+50, yy+10])
                    txt_g = font2.render(m1[4], True, (0,55,0))#登校
                    screen.blit(txt_g, [xx+200, yy+10])              
                    txt_g = font2.render(m1[5], True, (0,55,0))#下校
                    screen.blit(txt_g, [xx+350, yy+10])
                    if m1[6]=="体温" or m1[6]=="":
                        txt_g = font2.render(m1[6], True, (0,55,0))#体温
                    else:    
                        tmp=float(m1[6])
                        if tmp>=37.0:              
                            txt_g = font2.render(m1[6], True, (155,0,0))#体温赤で
                        else:    
                            txt_g = font2.render(m1[6], True, (0,55,0))#体温
                    screen.blit(txt_g, [xx+500, yy+10])    
                    #備考
                    btxt=m1[2]+m1[3]
                    txt_g = font2.render(btxt, True, (0,55,0))#備考
                    screen.blit(txt_g, [xx+600, yy+10])

                pygame.display.update()   
                for event in pygame.event.get(): 
                    if event. type == QUIT: 
                        pygame.quit() 
                        sys. exit()
                    elif event.type == KEYDOWN: 
                        isLoop=False
                        break
                if isLoop==False:
                    break    

            mrgs2csv(Tsets)
        elif jb==2:
            mes="ーーー登校時刻の設定ーーー"
            g_message.message0(Gsets,mes)#メッセージとサーフェス画像
            txt_g = font.render("現在の設定", True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [20, 450])                    # 画像を表示
            t2=str(Tsets["tokoh"])+":"+str(Tsets["tokom"])
            txt_g = font.render(t2, True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [20, 500])                    # 画像を表示
            txt_g = font.render("時(6-20)", True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [20, 550])                    # 画像を表示
            txt1=g_input.tbox(screen,font,300,550,50,50,4)
            txt_g = font.render("分(0-60)", True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [520, 550])                    # 画像を表示
            txt2=g_input.tbox(screen,font,800,550,50,50,4)
            Tsets["tokoh"]=int(txt1)
            Tsets["tokom"]=int(txt2)
        elif jb==3:
            mes="ーーー下校時刻の設定ーーー"
            g_message.message0(Gsets,mes)#メッセージとサーフェス画像
            txt_g = font.render("現在の設定", True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [20, 450])                    # 画像を表示
            t2=str(Tsets["gekoh"])+":"+str(Tsets["gekom"])
            txt_g = font.render(t2, True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [20, 500])                    # 画像を表示
            txt_g = font.render("時(6-20)", True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [20, 550])                    # 画像を表示
            txt1=g_input.tbox(screen,font,300,550,50,50,4)
            txt_g = font.render("分(0-60)", True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [520, 550])                    # 画像を表示
            txt2=g_input.tbox(screen,font,800,550,50,50,4)
            Tsets["gekoh"]=int(txt1)
            Tsets["gekom"]=int(txt2)
        if jb==8:
            return "n"
        if jb==9:
            mes="終了します "
            g_message.message(Gsets,mes)#メッセージとサーフェス画像
            return "y"

def toko(Gsets,id,id_list):
    mes="登校：今日も元気で行きましょう"
    #本人確認
    yn = g_kakunin.kakunin(Gsets,students,id,mes)
    if yn == 0:
        return #違うならここでreturn   
    #体温入力など
    mes=students[id]+"さん、おはようーーー"
    taion=g_input_taion.input_taion(Gsets,mes)
    id_list.append(id)
    #ログに記録
    now = datetime.datetime.now()
    #print(now)
    f=open ('rec/toko.log','a', encoding='utf-8')
    data=str(id)+","+students[id]+","+str(now)+","+str(taion)+"\n"
    f.write(data)
    f.close()

def geko(Gsets,id,id_list):
    mes="下校：お疲れ様でした"
    #本人確認
    yn = g_kakunin.kakunin(Gsets,students,id,mes)
    if yn == 0:
        return #違うならここでreturn   
    #ログに記録
    now = datetime.datetime.now()
    #(now)
    f=open ('rec/geko.log','a', encoding='utf-8')
    data=str(id)+","+students[id]+","+str(now)+"\n"
    f.write(data)
    f.close()
    #下校処理
    g_message.message(Gsets,students[id]+"さん、さようなら")
    id_list.remove(id)

class PersonalData():
    def __init__(self):
        self.id=""
        self.name=""
        self.toko=""
        self.geko=""
        self.toko_t=""
        self.geko_t=""
        self.taion=""

#グローバル
students=["江夏豊","村山実","若田緑","小林公示","榎本武揚","武田信玄","織田信長","徳川家康","新選組","佐々木小次郎"]

def main():
    pygame.init()                                 # Pygameの初期化
    screen = pygame.display.set_mode((1200, 800))  # 画面
    # font = pygame.font.SysFont("hg明朝b", 45)
    # font2 = pygame.font.SysFont("hg明朝b", 25)
    font = pygame.font.SysFont("hg明朝bhgp明朝bhgs明朝b", 45)
    font2 = pygame.font.SysFont("hg明朝bhgp明朝bhgs明朝b", 25)

    g1 = pygame.image.load("img/teacher.png").convert_alpha()   #絵を読み込む    
    Gsets=[screen,font,font2,g1]#グラフィックセット
    Tsets={"tokoh":8,"tokom":30,"gekoh":16,"gekom":0}    #当下校時刻のセット
    id_list = make_id_list()#ログデータを見て在校生徒を調べる、登校していて帰ってないならそのidがここに入る
    while True:
        mrgs = make_mrgs(Tsets)#表示用データ作成
        id=g_aisatu.aisatu(Gsets,len(students),mrgs)#挨拶画面と現時点の状況表示、idの入力
        mode=id2mode(id,id_list)#idからモードの決定
        if mode == "kyosi":
            yn = kyosi(Gsets,Tsets)#教師モード、完全終了時はyn="y"が返される
            if yn == "y":
                break
        elif mode == "toko":
            toko(Gsets,id,id_list)
        elif mode == "geko":
            geko(Gsets,id,id_list)    
    print("お疲れ様でした")            

main()
