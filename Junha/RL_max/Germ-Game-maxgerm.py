import numpy as np
import pickle
import sys


BOARD_ROWS = 7
BOARD_COLS = 7


class State:
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.board[0, 0] = self.board[BOARD_ROWS-1, BOARD_COLS-1] = 1
        self.board[BOARD_ROWS-1, 0] = self.board[0, BOARD_COLS-1] = -1
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        # init p1 plays first
        self.playerSymbol = 1
    
    # get unique hash of current board state
    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS*BOARD_ROWS))
        return self.boardHash
    
    def cantmove(self):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == 0:
                    self.board[i, j] = -self.playerSymbol
        return None
    
    def winner(self):
        # end
        if sum(map(sum, map(abs, self.board))) == BOARD_ROWS*BOARD_COLS:
            self.isEnd = True
            return sum(map(sum, self.board))
            """if sum(map(sum, self.board)) > 0:
                return 1
            else:
                return -1"""
        # not end
        self.isEnd = False
        return None
    
    def availablePositions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == self.playerSymbol:
                    for ii in range(-2,3):
                        for jj in range(-2,3):
                            if ii == 0 and jj == 0:
                                continue
                            if i + ii < 0 or i + ii >= BOARD_ROWS or j + jj < 0 or j + jj >= BOARD_COLS:
                                continue
                            if self.board[i + ii, j + jj] == 0:
                                positions.append((i, j, i + ii, j + jj))  # need to be tuple
        return positions
    
    def availablemaxPositions(self):
        mx = -1
        positions = self.availablePositions()
        mx_positions = []
        for p in positions:
            delta = 0
            next_board = self.board.copy()
                
            if max(abs(p[2] - p[0]), abs(p[3] - p[1])) == 2:
                next_board[p[0:2]] = 0
                delta -= 1
                
            dx1 = [-1, -1, -1, 0, 0, 1, 1, 1]
            dy1 = [-1, 0, 1, -1, 1, -1, 0, 1]
            next_board[p[2], p[3]] = self.playerSymbol
            delta += 1
            for dx, dy in zip(dx1, dy1):
                if p[2] + dx < 0 or p[2] + dx >= BOARD_ROWS or p[3] + dy < 0 or p[3] + dy >= BOARD_COLS:
                    continue
                if next_board[p[2] + dx, p[3] + dy] == -self.playerSymbol:
                    next_board[p[2] + dx, p[3] + dy] = self.playerSymbol
                    delta += 2
            
            if mx < delta:
                mx = delta
                mx_positions = []
            if mx == delta:
                mx_positions.append(p)
        return mx_positions
    
    def updateState(self, position):
        ii = position[2] - position[0]
        jj = position[3] - position[1]
        if max(abs(ii), abs(jj)) == 2:
            self.board[position[0:2]] = 0
        
        dx1 = [-1, -1, -1, 0, 0, 1, 1, 1]
        dy1 = [-1, 0, 1, -1, 1, -1, 0, 1]
        i, j = position[2:4]
        self.board[i, j] = self.playerSymbol
        for ii, jj in zip(dx1, dy1):
            if i + ii < 0 or i + ii >= BOARD_ROWS or j + jj < 0 or j + jj >= BOARD_COLS:
                continue
            if self.board[i + ii, j + jj] == -self.playerSymbol:
                self.board[i + ii, j + jj] = self.playerSymbol
            
        # switch to another player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1
    
    # only when game ends
    def giveReward(self):
        result = self.winner()
        # backpropagate reward
        self.p1.feedReward(result)
        self.p2.feedReward(-result)
        """if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        else:
            self.p1.feedReward(0)
            self.p2.feedReward(1)"""
    
    # board reset
    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.board[0, 0] = self.board[BOARD_ROWS-1, BOARD_COLS-1] = 1
        self.board[BOARD_ROWS-1, 0] = self.board[0, BOARD_COLS-1] = -1
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1
    
    def play(self, rounds=100):
        for i in range(rounds):
            if i%10 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                if not positions:
                    self.cantmove()
                else:
                    positions = self.availablemaxPositions()
                    p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                    # take action and upate board state
                    self.updateState(p1_action)
                # self.showBoard()
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                # check board status if it is end
                win = self.winner()
                if win is not None:
                    # self.showBoard()
                    # ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.availablePositions()
                    if not positions:
                        self.cantmove()
                    else:
                        positions = self.availablemaxPositions()
                        p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                        self.updateState(p2_action)
                    # self.showBoard()
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)
                    
                    win = self.winner()
                    if win is not None:
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break
    
    # play with human
    def play2(self):
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            if not positions:
                self.cantmove()
            else:
                # human
                # p1_action = self.p1.chooseAction(positions)
                # computer
                positions = self.availablemaxPositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action)
            self.showBoard()
            # check board status if it is end
            win = self.winner()
            if win is not None:
                if win > 0:
                    print(self.p1.name, "wins!")
                else:
                    print(self.p2.name, "wins!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions()
                if not positions:
                    self.cantmove()
                else:
                    # human
                    p2_action = self.p2.chooseAction(positions)
                    # computer
                    # positions = self.availablemaxPositions()
                    # p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    # take action and upate board state
                    self.updateState(p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    if win > 0:
                        print(self.p1.name, "wins!")
                    else:
                        print(self.p2.name, "wins!")
                    print()
                    self.reset()
                    break

    def showBoard(self):
        # p1: o  p2: x
        for i in range(0, BOARD_ROWS):
            print('------------------------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = 'o'
                if self.board[i, j] == -1:
                    token = 'x'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('------------------------------')


class Player:
    def __init__(self, name, exp_rate=0.1):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.95
        self.states_value = {}  # state -> value
    
    def getHash(self, board):
        boardHash = str(board.reshape(BOARD_COLS*BOARD_ROWS))
        return boardHash
    
    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                
                if max(abs(p[2] - p[0]), abs(p[3] - p[1])) == 2:
                    next_board[p[0:2]] = 0
                dx1 = [-1, -1, -1, 0, 0, 1, 1, 1]
                dy1 = [-1, 0, 1, -1, 1, -1, 0, 1]
                next_board[p[2], p[3]] = symbol
                for dx, dy in zip(dx1, dy1):
                    if p[2] + dx < 0 or p[2] + dx >= BOARD_ROWS or p[3] + dy < 0 or p[3] + dy >= BOARD_COLS:
                        continue
                    if next_board[p[2] + dx, p[3] + dy] == -symbol:
                        next_board[p[2] + dx, p[3] + dy] = symbol
                
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action
    
    # append a hash state
    def addState(self, state):
        self.states.append(state)
    
    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr*(self.decay_gamma*reward - self.states_value[st])
            reward = self.states_value[st]
            
    def reset(self):
        self.states = []
        
    def savePolicy(self, rounds):
        fw = open('policy_mx_legr_' + str(self.lr) + '_' + str(self.exp_rate) + '_' + str(self.decay_gamma) + '_' + str(rounds) + '_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file,'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name 
    
    def chooseAction(self, positions):
        for i in range(0,3):
        # while True:
            # for x in positions:
                # print(x)
            row1 = int(input("Input your action row1:"))
            col1 = int(input("Input your action col1:"))
            row2 = int(input("Input your action row2:"))
            col2 = int(input("Input your action col2:"))
            action = (row1, col1, row2, col2)
            if action in positions:
                return action
        sys.exit(1)
    
    # append a hash state
    def addState(self, state):
        pass
    
    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        pass
            
    def reset(self):
        pass


p1 = Player("p1")
p2 = Player("p2")

st = State(p1, p2)
print("training...")
st.play(1000)


p1.savePolicy(1000)
p2.savePolicy(1000)


# p1 = Player("computer1", exp_rate=0)
p1.loadPolicy("policy_mx_legr_0.2_0.1_0.95_1000_p1")
# p2 = Player("computer2", exp_rate=0)
# p2.loadPolicy("policy_mx_legr_0.2_0.1_0.95_1000_p2")

# p1 = HumanPlayer("human1")
p2 = HumanPlayer("human2")

st = State(p1, p2)
st.play2()
