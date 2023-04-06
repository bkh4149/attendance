import datetime
import pygame
from pygame.locals import *
import sys
import g_input

def aisatu(Gsets,num,mrgs):
    screen = Gsets[0]
    font = Gsets[1]
    font2 = Gsets[2]
    g1 = Gsets[3]
    #text作成
    today = datetime.date.today()
    today_txt="今日は"+str(today)+"です"
    id_txt="出席番号は何番ですか？"
    ms=["おはようー",today_txt,id_txt]

    while True:
        screen.fill((255,255,255))
        #ここに出欠表を書く
        pygame.draw.rect(screen, (0,155,0), Rect(550,100,600,650), 2)    # ■
        for i in range(len(mrgs)):
            m1=mrgs[i]
            yy=100+i*50
            pygame.draw.line(screen, (0,155,0), (550,yy+50), (1150,yy+50), 2)    # 線
            txt_g = font2.render(m1[0], True, (0,55,0))#ID
            screen.blit(txt_g, [570, yy+10])
            if m1[4]!="" and m1[5]=="":#校舎にいるなら              
                txt_g = font2.render(m1[1], True, (155,0,0))#名前赤で
            else:
                txt_g = font2.render(m1[1], True, (0,55,0))#名前
            screen.blit(txt_g, [600, yy+10])
            txt_g = font2.render(m1[4], True, (0,55,0))#登校
            screen.blit(txt_g, [750, yy+10])              
            txt_g = font2.render(m1[5], True, (0,55,0))#下校
            screen.blit(txt_g, [900, yy+10])
            if m1[6]=="体温" or m1[6]=="":
                txt_g = font2.render(m1[6], True, (0,55,0))#体温
            else:    
                tmp=float(m1[6])
                if tmp>=37.0:              
                    txt_g = font2.render(m1[6], True, (155,0,0))#体温赤で
                else:    
                    txt_g = font2.render(m1[6], True, (0,55,0))#体温
            screen.blit(txt_g, [1050, yy+10])              

        screen.blit(g1 ,Rect(300,330,50,50))        #先生の描画
        #文字の表示
        gy=100
        for m1 in ms: 
            txt_g = font.render(m1, True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [20, gy])                    # 画像を表示
            gy+=50

        id = g_input.tbox(screen,font,20,300,150,50,4)# 文字を入力  
        id2=int(id)
        if 0 <= id2 < num or id2==999:
            return id2

        pygame.display.update()                        # 画面更新
        # イベント処理
        for event in pygame.event.get():  # イベントを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら
                pygame.quit()             
                sys.exit()                # 終了
# pygame.init()                                 # Pygameの初期化
# screen = pygame.display.set_mode((1200, 800))  # 画面
# font = pygame.font.SysFont("hg明朝b", 45)
# font2 = pygame.font.SysFont("hg明朝b", 25)
# g1 = pygame.image.load("img/teacher.png").convert_alpha() 
# Gsets=[screen,font,font2,g1]
# students=["青木一郎","井田美智子","内田稔","江本由紀","大山昇","神田和夫","霧島洋子","栗田雅彦","菰田真紀","佐々木正明"]
# num=len(students)
# Tsets={"tokoh":8,"tokom":30,"gekoh":16,"gekom":0} 
# #def make_mrgs(Tsets):
# mrgs = t2.make_mrgs(Tsets)
# aisatu(Gsets,num,mrgs)
