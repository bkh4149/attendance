import datetime
import pygame
from pygame.locals import *
import sys
import g_input
import g_message
def input_taion(Gsets,mes):
    pygame.init()                                 # Pygameの初期化
    screen = Gsets[0]
    font = Gsets[1]
    g1a = pygame.image.load("img/ondo.png").convert_alpha()   #温度計の絵（50x50）を読み込む
    g1 = pygame.transform.rotozoom(g1a, 0, 0.5)
    g2a = pygame.image.load("img/netu.png").convert_alpha()   #熱があるの絵（50x50）を読み込む
    g2 = pygame.transform.rotozoom(g2a, 0, 0.5)
    gold=Gsets[3]
    ms=[mes,"パソコンの近くに体温計があるので測ってね！","測った体温は何度ですか？"]
    while True:
        screen.fill((255,255,255))
        screen.blit(g1 ,Rect(300,330,50,50))        #描画
        #文字の表示
        gy=100
        for m1 in ms: 
            txt_g = font.render(m1, True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [20, gy])                    # 画像を表示
            gy+=50
        id = g_input.tbox(screen,font,20,300,150,50,4)# 文字を入力  
        id2=float(id)
        #print("@27 id2=",id2)
        if 35 <= id2 < 37:
            return id2
        elif 37 <= id2 < 42:
            Gsets[3]=g2
            g_message.message(Gsets,"熱があるようだね。先生に相談しよう。")
            Gsets[3]=gold
            return id2
        else:    
            g_message.message(Gsets,"もう一度、ちゃんと体温を測ってみてね！")
        pygame.display.update()                        # 画面更新
        # イベント処理
        for event in pygame.event.get():  # イベントを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら
                pygame.quit()             
                sys.exit()                # 終了
