import copy

di={1:-1,2:-1,3:-1,4:0,6:0,7:1,8:1,9:1}
dj={1:-1,2:0,3:1,4:-1,6:1,7:-1,8:0,9:1}#向きのdata

def ct(turn):
    if turn=="o":return "x"
    else:return "o"

def reset(board):
    # board=[[" "]]#初期配置
    for i in range(1,9):
        board[0].append(i)
        board.append([i]+["-"]*8)
    board[4][4],board[4][5],board[5][4],board[5][5]="o","x","x","o"
    return board

def t_o(y1,x1,p,d,plate):#裏返す(y1:i座標,x:j座標,p:駒("o","x"),d:向き,board:盤)turn_over,向き1:左上,2:上,3:右上,4:左,6:右,7:左下,8:下,9:右下
    if (x1==1 and d%3==1)or(x1==8 and d%3==0)or(y1==1 and d<=3)or(y1==8 and d>=7):#判定マスが枠外
        return 0
    if x1<=0 or y1<=0 or x1>8 or y1>8 or plate[y1][x1] in [p,"-"]:
        return 0    
    if d in [4,6]:
        if d==4 :y2,x2=y1,x1-1
        if d==6:y2,x2=y1,x1+1
    else:
        y2,x2=y1+di[d],x1+dj[d]
    t_o(y2,x2,p,d,plate)
    if plate[y2][x2]==p:
        plate[y1][x1]=p
    return 0

def tf_judge(y,x,board,turn):#入力できるかの判定
    if not (1<=x and x<=8 and 1<=y and y<=8):
        return False
    if board[y][x] in ["o","x"]:
        return False

    memo=copy.deepcopy(board)
    for i in range(1,10):
        if i==5:continue
        t_o(y+di[i],x+dj[i],turn,i,memo)
    if board!=memo:return True
    else:return False

def judge(board,turn):#おける場所があるかの判定
    n=0
    for i in range(1,9):
        for j in range(1,9):
            if tf_judge(i,j,board,turn):n+=1

    if n==0:return True
    else:return False

def win(board):
    count_o,count_x=0,0
    for i in range(1,9):
        for j in range(1,9):
            if board[i][j]=="o":count_o+=1
            if board[i][j]=="x":count_x+=1

    if count_o>count_x:return "o"
    elif count_x>count_o:return "x"
    elif count_o==count_x:return "draw"

def reversi(y,x,board,turn):#return[turn,"左上の出力文字",出力するか,時間(100000以上なら消えない)]
    if tf_judge(y,x,board,turn):
        board[y][x]=turn
        for i in range(1,10):
            if i==5:continue
            t_o(y+di[i],x+dj[i],turn,i,board)

        turn=ct(turn)
        if judge(board,turn):
            turn=ct(turn)            
            if judge(board,turn):
                win_p=win(board)
                if win_p=="draw":#決着
                    return [turn,"draw, Tap to [r]eset",True,10000]
                elif win_p=="o":
                    return [turn,"白 win, Tap to [r]eset",True,10000]
                elif win_p=="x":
                    return [turn,"黒 win, Tap to [r]eset",True,10000]
            
            return [turn,"pass",True,5000]

    else:
        return[turn,"入力できねぇって",True,5000]
    return [turn,"",False,0]