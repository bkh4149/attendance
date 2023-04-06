import datetime
import pygame
from pygame.locals import *
import sys
import g_input

def kyosi(Gsets):
    screen = Gsets[0]
    font = Gsets[1]
    #text作成
    ms=["メニューを選択してください","1:CSV記録作成","2:登校時刻設定","3:下校時刻設定","8:抜ける","9:完全終了"]

    while True:
        screen.fill((255,255,255))
        #メニューの表示
        gy=100
        for m1 in ms: 
            txt_g = font.render(m1, True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [20, gy])                    # 画像を表示
            gy+=50

        id = g_input.tbox(screen,font,20,500,150,50,4)# 文字を入力  
        id2=int(id)
        if 1 <= id2 <= 5 or 8<=id2<=9:
            return id2

        pygame.display.update()                        # 画面更新
        # イベント処理
        for event in pygame.event.get():  # イベントを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら
                pygame.quit()             
                sys.exit()                # 終了

