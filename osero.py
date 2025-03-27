import pygame
import copy
import f

setting_name=["先行の色","黒担当","白担当","cpu lv.","位置ガイド","cpu待機時間"]
setting_data=[["白","黒"],["cpu","player"],["cpu","player"],[1,2,3],["ON","OFF"],[0,1000,3000,5000,9999]]#設定の選択肢
setting_save=[1,1,1,1,1,1]

board=[[" "]]
f.reset(board)
turn="x"

board_choice=[["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,]


#期待値
expect_value=[[10,3,4,5,5,4,3,10],
              [3,1,2,2,2,2,1,3],
              [4,2,3,3,3,3,2,4],
              [5,2,3,0,0,3,2,5],
              [5,2,3,0,0,3,2,5],
              [4,2,3,3,3,3,2,4],
              [3,1,2,2,2,2,1,3],
              [10,3,4,5,5,4,3,10]]

pygame.init()

sc_size=400#基本400
screen=pygame.display.set_mode((sc_size,sc_size))#1マス40*8+枠40*2,文字のスペース
pygame.display.set_caption("osero game")

font1=pygame.font.SysFont("hgｺﾞｼｯｸm",int(sc_size/100*6))
font2=pygame.font.SysFont("hgｺﾞｼｯｸm",int(sc_size/100*8))

def draw_line():
    for i in range(9):
        pygame.draw.line(screen,(0,0,0),(sc_size/10,(i+1)*sc_size/10),(sc_size*9/10,(i+1)*sc_size/10),3)
        pygame.draw.line(screen,(0,0,0),((i+1)*sc_size/10,sc_size/10),((i+1)*sc_size/10,sc_size*9/10),3)

def draw_piece(x,y):
    if board[y][x]=="o":#o:白,x:黒
        pygame.draw.circle(screen,(255,255,255),(x*sc_size/10+sc_size/20,y*sc_size/10+sc_size/20),sc_size/25)
    else:
        pygame.draw.circle(screen,(0,0,0),(x*sc_size/10+sc_size/20,y*sc_size/10+sc_size/20),sc_size/25)

def draw_board():
    for i in range(1,9):#盤の表示
        for j in range(1,9):
            if board[i][j] in ["o","x"]:
                draw_piece(j,i)

def extract_board_choice():
    for i in range(1,9):
        for j in range(1,9):
            if f.tf_judge(i,j,board,turn):
                board_choice[i-1][j-1]="~"

def draw_board_choice():#置ける場所を表示する
    for i in range(1,9):
        for j in range(1,9):
            if board_choice[i-1][j-1]=="~":
                pygame.draw.circle(screen,(255,255,0),(j*sc_size/10+sc_size/20,i*sc_size/10+sc_size/20),sc_size/50)

def stg_acs(choice):#選択肢の選択要素抽出
    return setting_data[choice][setting_save[choice]]              

text1=["",False,0]#左上の文字関数[表示文字,表示するか,時間9999まで]
def text1_p(text):#左上
    txt=font1.render(text,True,(0,0,0))
    screen.blit(txt,(sc_size/10,sc_size/100*3))

def text2_p(text):#右上
    txt=font2.render(text,True,(0,0,0))
    screen.blit(txt,(sc_size/10,sc_size/10*9+sc_size/100))

def cpu(lev):#cpu 1:最弱,2:普通,3:最強
    global turn
    global text1
    if lev in [1,2]:
        if lev==1:a=-1#調整倍数
        else:a=1
        e_v=[0,0,-100]#x,y,期待値
        for i in range(1,9):
            for j in range(1,9):
                if f.tf_judge(i,j,board,turn) and e_v[2]<expect_value[i-1][j-1]*a:
                    e_v=[j,i,expect_value[i-1][j-1]*a]
                    
        op_l=f.reversi(e_v[1],e_v[0],board,turn)
        if op_l[2] and text1[2]<10000:
            text1=[op_l[1],True,op_l[3]]
        turn=op_l[0]
        

    return 0


def setting():#設定画面
    def text_s(text,j,i,serect):#j:文字始まりのxマス目,i:文字始まりのｙマス目,serect:選択しているか（色を反転させる）
        if serect:
            txt=font1.render(text,True,(0,0,0),(0,230,0))
        else:
            txt=font1.render(text,True,(0,230,0))

        screen.blit(txt,(j*sc_size/10+sc_size/100*2,i*sc_size/10+sc_size/100*2))

    choice=0
    while True:
        screen.fill((230,230,230))

        #上記の文字表示
        pygame.draw.rect(screen,(15,15,15),(sc_size/10,sc_size/10,sc_size*8/10,sc_size*8/10))
        pygame.draw.rect(screen,(15,15,15),(sc_size/10,sc_size/100*2,sc_size/100*27,sc_size/100*9),3)     
        text1_p(" setting   Top to [b]ack")

        for i in range(len(setting_data)):#選択肢の表示
            text_s(f"{setting_name[i]}",1,i+2,False)
            if choice==i:
                text_s(f"<　{stg_acs(i)}　>",5,i+2,True)
            else:
                text_s(f"<　{stg_acs(i)}　>",5,i+2,False)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return
                if event.key==pygame.K_b:
                    return
                
                if event.key==pygame.K_DOWN:
                    choice+=1
                    choice%=len(setting_data)
                if event.key==pygame.K_UP:
                    choice-=1
                    choice%=len(setting_data)
                if event.key==pygame.K_RIGHT:
                    setting_save[choice]+=1
                    setting_save[choice]%=len(setting_data[choice])
                if event.key==pygame.K_LEFT:
                    setting_save[choice]-=1
                    setting_save[choice]%=len(setting_data[choice])

        
        pygame.display.update()


# time=0
cool_timer=0
extract_board_choice()
run=True
while run:#メイン処理
    screen.fill((255,255,255))

    pygame.draw.rect(screen, (0,200,0), (sc_size/10,sc_size/10,sc_size*8/10,sc_size*8/10))
    draw_line()    
    draw_board()
    if stg_acs(4)=="ON":#位置ガイド
        draw_board_choice()

    if text1[1] and text1[2]>0:#左上文字の表示タイマー
        text1_p(text1[0])
        if text1[2]<10000:
            text1[2]-=1

    if cool_timer>0:cool_timer-=1#playerが置いてからcpuが置くまでの時間

    if ((stg_acs(1)=="cpu" and turn=="x") or (stg_acs(2)=="cpu" and turn=="o")) and cool_timer==0 and text1[2]<10000:#cpu
        cpu(stg_acs(3))
        cool_timer=stg_acs(5)
        board_choice=[["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,]
        extract_board_choice()


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                run=False

            if event.key==pygame.K_r:#リセット
                board=[[" "]]
                f.reset(board)
                if stg_acs(0)=="黒":turn="x"
                else:turn="o"
                text1=["",False,0]
                cool_timer=stg_acs(5)*2
                board_choice=[["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,]
                extract_board_choice()

            if event.key==pygame.K_s:#設定画面に変更
                setting()

        if event.type==pygame.MOUSEBUTTONDOWN:#クリック操作
            x,y=pygame.mouse.get_pos()
            x=int(x//(sc_size/10))
            y=int(y//(sc_size/10))
            op_l=f.reversi(y,x,board,turn)
            if op_l[2] and text1[2]<10000:
                text1=[op_l[1],True,op_l[3]]
            turn=op_l[0]
            cool_timer=stg_acs(5)
            board_choice=[["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,["-"]*8,]
            extract_board_choice()


    if turn=="o":text2_p("白のターン") 
    else:text2_p("黒のターン") 
    # time+=1
    # text2_p(str(time))

    pygame.display.update()

pygame.quit()