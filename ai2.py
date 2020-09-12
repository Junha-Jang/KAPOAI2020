import sys
import random
import pickle
from copy import deepcopy

BOARD_ROWS = 7
BOARD_COLS = 7
INF = 1e9

B = []

def getHash(A, position, player):
    AA = deepcopy(A)
    p = position.copy()
    
    if p[2] - p[0] < 0:
        for i in range(3):
            for j in range(3):
                AA[i][j], AA[6-i][j] = AA[6-i][j], AA[i][j]
        p[0] = 6 - p[0]
        p[2] = 6 - p[2]

    if p[3] - p[1] < 0:
        for i in range(7):
            for j in range(7):
                AA[i][j], AA[i][6-j] = AA[i][6-j], AA[i][j]
        p[1] = 6 - p[1]
        p[3] = 6 - p[3]

    if p[2] - p[0] < p[3] - p[1]:
        for i in range(7):
            for j in range(i+1,7):
                AA[i][j], AA[j][i] = AA[j][i], AA[i][j]
        p[0], p[1] = p[1], p[0]
        p[2], p[3] = p[3], p[2]
        
    s1 = s2 = s3 = 0
    e2 = e3 = 0
    shape = 0

    for dx in range(-3,4):
        for dy in range(-3,4):
            if not dx and not dy:
                continue
            if p[0] + dx < 0 or p[0] + dx >= BOARD_ROWS or p[1] + dy < 0 or p[1] + dy >= BOARD_COLS:
                continue

            if AA[p[0] + dx][p[1] + dy] != 3 - player:
                continue
            if max(abs(dx), abs(dy)) == 1:
                s1 = 1
            if max(abs(dx), abs(dy)) == 2:
                s2 = 1
            if max(abs(dx), abs(dy)) == 3:
                s3 = 1

    for dx in range(-3,4):
        for dy in range(-3,4):
            if abs(dx) <= 1 and abs(dy) <= 1:
                continue
            if p[2] + dx < 0 or p[2] + dx >= BOARD_ROWS or p[3] + dy < 0 or p[3] + dy >= BOARD_COLS:
                continue

            if AA[p[2] + dx][p[3] + dy] != 3 - player:
                continue
            if max(abs(dx), abs(dy)) == 2:
                e2 = 1
            if max(abs(dx), abs(dy)) == 3:
                e3 = 1

    for dx in range(-1,2):
        for dy in range(-1,2):
            if not dx and not dy:
                continue

            shape = shape << 1
            if p[2] + dx < 0 or p[2] + dx >= BOARD_ROWS or p[3] + dy < 0 or p[3] + dy >= BOARD_COLS:
                shape = shape | 1
            elif AA[p[2] + dx][p[3] + dy]:
                shape = shape | 1

    if(p[3] - p[1] < 2):
        return ((p[3] - p[1]) << 12) + ((s1 | s2) << 11) + (s3 << 10) + (e2 << 9) + (e3 << 8) + shape + 1
    return ((p[3] - p[1]) << 12) + (s1 << 11) + (s2 << 10) + (e2 << 9) + (e3 << 8) + shape + 1

def next_board(A, p, player):
    AA = deepcopy(A)
    if p[0] == -1:
        for x in range(BOARD_ROWS):
            for y in range(BOARD_COLS):
                if AA[x][y] == 0:
                    AA[x][y] = 3 - player
        return AA
 
    AA[p[2]][p[3]] = player
    if max(abs(p[2] - p[0]), abs(p[3] - p[1])) == 2:
        AA[p[0]][p[1]] = 0
    for x in range(max(p[2] - 1, 0), min(p[2] + 2, BOARD_ROWS)):
    	for y in range(max(p[3] - 1, 0), min(p[3] + 2, BOARD_COLS)):
            if AA[x][y] == 3 - player:
                AA[x][y] = player
    return AA


def score(A, player):
    scr = 0
    for x in range(BOARD_ROWS):
        for y in range(BOARD_COLS):
            if A[x][y] == player:
                scr += 1
            elif A[x][y] == 3 - player:
                scr -= 1
    return scr
 
 
def all_move(A, player):
    plist = []
    for x1 in range(BOARD_ROWS):
        for y1 in range(BOARD_COLS):
            if A[x1][y1] != player:
                continue
            for x2 in range(max(x1 - 2, 0), min(x1 + 3, BOARD_ROWS)):
                for y2 in range(max(y1 - 2, 0), min(y1 + 3, BOARD_COLS)):
                    if A[x2][y2] == 0:
                        plist.append([x1, y1, x2, y2])
    return plist
 
 
def rand_move(player):
    plist = all_move(B, player)
    if not plist:
        return [-1, -1, -1, -1]
    return random.choice(plist)
 
 
def get_phase(player):
    cnt = 0
    for x in range(BOARD_ROWS):
        for y in range(BOARD_COLS):
            if B[x][y] != 0:
                cnt += 1
    if cnt >= BOARD_ROWS * BOARD_COLS - 4:
        return 3
 
    for x1 in range(BOARD_ROWS):
        for y1 in range(BOARD_COLS):
            if B[x1][y1] != player:
                continue
            for x2 in range(max(x1 - 3, 0), min(x1 + 4, BOARD_ROWS)):
                for y2 in range(max(y1 - 3, 0), min(y1 + 4, BOARD_COLS)):
                    if B[x2][y2] == 3 - player:
                        return 2
    return 1
 
 
def phase1(player):
    cntu = cntd = cntl = cntr = 0
    for x in range(BOARD_ROWS):
        for y in range(BOARD_COLS):
            if B[x][y] != 3 - player:
                continue
            if x >= y:
                if 6-x >= y:
                    cntl += 1
                if 6-x <= y:
                    cntd += 1
            if x <= y:
                if 6-x >= y:
                    cntu += 1
                if 6-x <= y:
                    cntr += 1
 
    p = []
    mx = max(max(cntu, cntd), max(cntl, cntr))
    if mx == cntu:
        if B[0][6] == player and B[1][5] == 0:
            p = [0, 6, 1, 5]
        elif B[1][5] == player and B[2][4] == 0:
            p = [1, 5, 2, 4]
        elif B[2][4] == player and B[1][4] == 0:
            p = [2, 4, 1, 4]
        elif B[2][4] == player and B[2][5] == 0:
            p = [2, 4, 2, 5]
        elif B[6][0] == player and B[5][1] == 0:
            p = [6, 0, 5, 1]
        elif B[5][1] == player and B[4][2] == 0:
            p = [5, 1, 4, 2]
        elif B[4][2] == player and B[4][1] == 0:
            p = [4, 2, 4, 1]
        elif B[4][2] == player and B[5][2] == 0:
            p = [4, 2, 5, 2]
        else:
            p = rand_move(player)
    elif mx == cntd:
        if B[6][0] == player and B[5][1] == 0:
            p = [6, 0, 5, 1]
        elif B[5][1] == player and B[4][2] == 0:
            p = [5, 1, 4, 2]
        elif B[4][2] == player and B[5][2] == 0:
            p = [4, 2, 5, 2]
        elif B[4][2] == player and B[4][1] == 0:
            p = [4, 2, 4, 1]
        elif B[0][6] == player and B[1][5] == 0:
            p = [0, 6, 1, 5]
        elif B[1][5] == player and B[2][4] == 0:
            p = [1, 5, 2, 4]
        elif B[2][4] == player and B[2][5] == 0:
            p = [2, 4, 2, 5]
        elif B[2][4] == player and B[1][4] == 0:
            p = [2, 4, 1, 4]
        else:
            p = rand_move(player)
    elif mx == cntl:
        if B[6][0] == player and B[5][1] == 0:
            p = [6, 0, 5, 1]
        elif B[5][1] == player and B[4][2] == 0:
            p = [5, 1, 4, 2]
        elif B[4][2] == player and B[4][1] == 0:
            p = [4, 2, 4, 1]
        elif B[4][2] == player and B[5][2] == 0:
            p = [4, 2, 5, 2]
        elif B[0][6] == player and B[1][5] == 0:
            p = [0, 6, 1, 5]
        elif B[1][5] == player and B[2][4] == 0:
            p = [1, 5, 2, 4]
        elif B[2][4] == player and B[1][4] == 0:
            p = [2, 4, 1, 4]
        elif B[2][4] == player and B[2][5] == 0:
            p = [2, 4, 2, 5]
        else:
            p = rand_move(player)
    elif mx == cntr:
        if B[0][6] == player and B[1][5] == 0:
            p = [0, 6, 1, 5]
        elif B[1][5] == player and B[2][4] == 0:
            p = [1, 5, 2, 4]
        elif B[2][4] == player and B[2][5] == 0:
            p = [2, 4, 2, 5]
        elif B[2][4] == player and B[1][4] == 0:
            p = [2, 4, 1, 4]
        elif B[6][0] == player and B[5][1] == 0:
            p = [6, 0, 5, 1]
        elif B[5][1] == player and B[4][2] == 0:
            p = [5, 1, 4, 2]
        elif B[4][2] == player and B[5][2] == 0:
            p = [4, 2, 5, 2]
        elif B[4][2] == player and B[4][1] == 0:
            p = [4, 2, 4, 1]
        else:
            p = rand_move(player)
    return p
 
 
def phase23(A, dep, player):
    if dep == 0 :
        return [-1, -1, -1, -1, score(A, player)]
 
    mx1 = -INF
    mxp1 = []
    plist1 = all_move(A, player)
    if not plist1:
        p1 = [-1, -1, -1, -1]
        AA = next_board(A, p1, player)
        p1.append(score(AA, player))
        return p1
 
    for p1 in plist1:
        AA = next_board(A, p1, player)
        mn2 = INF
        plist2 = all_move(AA, 3 - player)
        if not plist2:
            p2 = [-1, -1, -1, -1]
            AAA = next_board(AA, p2, 3 - player)
            mn2 = score(AAA, player)
 
        for p2 in plist2:
            AAA = next_board(AA, p2, 3 - player)
            res = phase23(AAA, dep - 1, player)
            mn2 = min(mn2, res[4])
        if mx1 < mn2:
            mx1 = mn2
            mxp1 = []
            mxp1.append(p1)
        elif mx1 == mn2:
            mxp1.append(p1)

    fr = open('policy3_legr_0.2_0.1_0.95_1000_p2', 'rb')
    states_value = pickle.load(fr)
    fr.close()

    value_max = -INF
    for p in mxp1:
        boardHash = getHash(A, p, player)
        value = 0 if states_value.get(boardHash) is None else states_value.get(boardHash)
        if value >= value_max:
            value_max = value
            action = p

    action.append(mx1)
    return action


if __name__ == "__main__":

    input_str = sys.stdin.read()

    # file = open("file.txt")
    # input_str = file.read()
    # print(input_str)

    # 입력 예시
    # READY 1234567890.1234567 (입력시간)
    # "OK" 를 출력하세요.
    if input_str.startswith("READY"):
        # 출력
        sys.stdout.write("OK")

    # 입력 예시
    # PLAY
    # 1 0 0 0 0 0 2
    # 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0
    # 0 0 0 0 0 0 0
    # 2 0 0 0 0 0 1
    # 1234567890.1234567 (입력시간)

    # AI의 액션을 출력하세요.
    # 출력 예시 : "0 0 2 2"
    elif input_str.startswith("PLAY"):
        player = 1 if __file__[-4] == '1' else 2

        # make board
        input_lines = input_str.split("\n")
        for i in range(BOARD_ROWS):
            B.append(list(map(int, input_lines[i+1].split(" "))))

        idx = get_phase(player)
        p = []
        if idx == 1:
            p = phase1(player)
        elif idx == 2:
            p = phase23(B, 1, player)[0:4]
        elif idx == 3:
            p = phase23(B, 2, player)[0:4]

        # 출력
        if p[0] == -1:
            p = random.choice([])
        sys.stdout.write(f"{p[0]} {p[1]} {p[2]} {p[3]}")