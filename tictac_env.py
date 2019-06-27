import random
import tkinter as ts
import copy


class TicTac(object):
    def __init__(self):
        self.n_actions = 9
        self.win_case = [[0,4,8],[2,4,6],[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8]]

    def reset(self):

        return 9 * [0]

    def step(self,action,current_board,agent='first'):
        board = copy.deepcopy(current_board)
 
        if board[action] == 1 or board[action] == 2:
            reward = -1
            s_ = board
            done = False

        if board[action] == 0:
            assert agent == 'first' or agent == 'second', 'please type first or second'
            if agent == 'first':
                board[action] = 1 

                if self.check_win(board) == 1:
                    reward = 100
                    done = True
                    s_ = 'win'
            
                else:
                    reward = 0
                    done = False
                    s_ = board

            if agent == 'second':
                board[action] = 2

                if self.check_win(board) == 2:
                    reward = 100
                    done = True
                    s_ = 'win'
            
                else:
                    reward = 0
                    done = False
                    s_ = board

        return s_, reward, done

    def lose(self):
        reward = -100
        state_ = 'lose'

        return reward, state_

    def check_win(self,board):
        for i in self.win_case:
            if board[i[0]] == 1 and board[i[1]] == 1 and board[i[2]] == 1:
                return 1
            if board[i[0]] == 2 and board[i[1]] == 2 and board[i[2]] == 2:
                return 2

    def check_over(self,board):
        if 0 in board:
            return False
        else:
            return True
    
    def drawBoard(self, board) :
        key = {0:' ', 1:'X', 2:'O'}
        print('################')
        print(" " + key[board[6]] + " | " + key[board[7]] + " | " + key[board[8]])
        print("------------")
        print(" " + key[board[3]] + " | " + key[board[4]] + " | " + key[board[5]])
        print("------------")
        print(" " + key[board[0]] + " | " + key[board[1]] + " | " + key[board[2]])
        print('################')