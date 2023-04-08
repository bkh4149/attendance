import pygame
from pygame.locals import *
import sys
import time

def message(Gsets,mes):#メッセージとサーフェス画像
    screen=Gsets[0]
    font = Gsets[1]
    g1=Gsets[3]        
    a_txt=mes
    b_txt="okならエンターを押してね"
    while True:
        screen.fill((255,255,255))
        screen.blit(g1 ,Rect(330,300,50,50))        #先生の描画
        txt_g = font.render(a_txt, True, (55,55,55)) # 描画する文字列を画像にする
        screen.blit(txt_g, [20, 100])                    # 画像を表示
        txt_g = font.render(b_txt, True, (55,55,55)) # 描画する文字列を画像にする
        screen.blit(txt_g, [20, 200])  
        pygame.display.update()   
        for event in pygame.event.get(): 
            if event. type == QUIT: 
                pygame.quit() 
                sys. exit()
            elif event.type == KEYDOWN: 
                return

def message0(Gsets,mes):#メッセージとサーフェス画像 勝手に戻る
    screen=Gsets[0]
    font = Gsets[1]
    g1=Gsets[3]        
    a_txt=mes
    screen.fill((255,255,255))
    screen.blit(g1 ,Rect(330,300,50,50))        #先生の描画
    txt_g = font.render(a_txt, True, (55,55,55)) # 描画する文字列を画像にする
    screen.blit(txt_g, [20, 100])                    # 画像を表示
    pygame.display.update()   

def message3(Gsets,mes):#メッセージとサーフェス画像 ３秒後に勝手に戻る
    screen=Gsets[0]
    font = Gsets[1]
    g1=Gsets[3]        
    a_txt=mes
    screen.fill((255,255,255))
    screen.blit(g1 ,Rect(330,300,50,50))        #先生の描画
    txt_g = font.render(a_txt, True, (55,55,55)) # 描画する文字列を画像にする
    screen.blit(txt_g, [20, 100])                    # 画像を表示
    pygame.display.update()   
    time.sleep(3)


