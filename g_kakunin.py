import datetime
import pygame
from pygame.locals import *
import sys
import g_input

#生徒の確認　id番号と名前が一致するか　答えはy/n　1/0
def kakunin(Gsets,students,id,mes):
    screen=Gsets[0]
    font = Gsets[1]
    g1=Gsets[3]
    ms=[mes,students[id]+"さん、ですよね？","yesなら1、noなら0で答えてね！"]
    while True:
        screen.fill((255,255,255))
        #先生の描画
        screen.blit(g1 ,Rect(300,330,50,50))
        #文字の表示
        gy=100
        for m1 in ms: 
            txt_g = font.render(m1, True, (55,55,55)) # 描画する文字列を画像にする
            screen.blit(txt_g, [20, gy])                    # 画像を表示
            gy+=50
        id = g_input.tbox(screen,font,20,300,150,50,4)# 文字を入力  
        id2=int(id)
        if id2==0 or id2==1:
          return id2
        pygame.display.update()                        # 画面更新

        # イベント処理
        for event in pygame.event.get():  # イベントを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら
                pygame.quit()             
                sys.exit()                # 終了

if __name__ == "__main__":
    pygame.init()                                 # Pygame初期化
    screen = pygame.display.set_mode((1000, 800))  # 800*600の画面
    g1 = pygame.image.load("img/teacher.png").convert_alpha() 
    students=["青木一郎","井田美智子","内田稔","江本由紀","大山昇","神田和夫","霧島洋子","栗田雅彦","菰田真紀","佐々木正明"]
    mes="konntiha"
    yn = kakunin(screen,students,1,mes,g1)
    print(yn)
