import pygame
from pygame.locals import *
import sys
def tbox(screen,font,x,y,w,h,n):
    txt=""
    isEnd=False#終了フラグ
    while True:
        pygame.draw.rect(screen, (255,255,0), Rect(x,y,w,h)) #ボックス内を塗潰す
        txtg = font.render(txt, True, (55,55,55)) # 描画する文字列を画像にする
        screen.blit(txtg, [x+5, y+5])             # 画像を表示        
        pygame.display.update()                   # 画面更新
       
        # イベント処理
        for event in pygame.event.get():  # イベントを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら
                pygame.quit()             
                sys.exit()                # 終了

            elif event.type == KEYDOWN:
              if event.key==K_LEFT  or event.key==K_BACKSPACE:#修正で戻る
                if len(txt)>=1:
                  txt = txt[:-1] 
              elif event.key==K_RETURN:#エンターキー
                isEnd=True
                break

              if len(txt)<n: 
                if event.key==K_PERIOD:#ピリオドが入力された
                  #print(".",end="")  
                  txt+="."
                else: 
                  for i in range(10):#0-9キーが入力された
                    if event.key==48+i:
                      #print(i,end="")  
                      txt+=str(i)
                      break

        if isEnd==True:
          break
    #print() 
    return txt

