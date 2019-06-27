from tictac_env import TicTac
from QLearn import QLearn
from Sarsa import Sarsa
import argparse
import copy
import os


Training_round = 100000 

def train(args):
    env = TicTac()
    if args.algorithm == 'Q-learning': 
        model1 = QLearn(actions=list(range(env.n_actions))) 
        model2 = QLearn(actions=list(range(env.n_actions))) 
    if args.algorithm == 'Sarsa': 
        model1 = Sarsa(actions=list(range(env.n_actions)))
        model2 = Sarsa(actions=list(range(env.n_actions)))

    first_win, second_win, tie = 0, 0, 0
    for epoch in range(Training_round):
        state1 = env.reset()
        while True:
            # The first agent step and learn
            action1 = model1.choose_action(state1)
            state1_, reward1, done = env.step(action1,state1,agent='first')
            model1.learn(state1,action1,reward1,state1_)
            while state1_ == state1:
                action1 = model1.choose_action(state1)
                state1_, reward1, done = env.step(action1,state1,agent='first')
                model1.learn(state1,action1,reward1,state1_)     
            
            if done:
                reward2, state2_ = env.lose()
                model2.learn(state2,action2,reward2,state2_)
                first_win += 1
                break

            if env.check_over(state1_):
                tie += 1
                break

            # The second agent step and learn
            state2 = copy.deepcopy(state1_)
            action2 = model2.choose_action(state2)
            state2_, reward2, done = env.step(action2,state2,agent='second')
            model2.learn(state2,action2,reward2,state2_)
            while state2_ == state2:
                action2 = model2.choose_action(state2)
                state2_, reward2, done = env.step(action2,state2,agent='second')
                model2.learn(state2,action2,reward2,state2_) 

            if done: 
                reward1, state1_ = env.lose()        
                model1.learn(state1,action1,reward1,state1_)
                second_win += 1
                break
            state1 = copy.deepcopy(state2_)

        print('first_win', first_win)
        print('second_win', second_win)
        print('tie', tie)
        percent = float(epoch*100)/Training_round
        print('training process: %.2f' % percent, '%')

    # save Q table 
    model1.save_table('Q_table', 'Q_learn1')
    model2.save_table('Q_table', 'Q_learn2')

def play(args):
    print('start to play the game')
    print('################')
    print(' ' + '6' + ' | ' + '7' + ' | ' + '8')
    print('------------')
    print(' ' + '3' + ' | ' + '4' + ' | ' + '5')
    print('------------')
    print(' ' + '0' + ' | ' + '1' + ' | ' + '2')
    print('################')
    print('please type 0 ~ 8 to selcet the place')
    print('please select the order 1. first (you go first) or 2. second (AI go first)')
    mode = input('mode: ')
    assert mode == 'first' or mode == 'second', 'please type first or second'
    
    env_play = TicTac()
    if args.algorithm == 'Q-learning': model = QLearn(actions=list(range(env_play.n_actions))) 
    if args.algorithm == 'Sarsa': model = Sarsa(actions=list(range(env_play.n_actions)))
    if mode == 'first':
        model.load_table('Q_table', 'Q_learn2')
        board = env_play.reset()
        env_play.drawBoard(board)
        while True:
            choice = human_input(board)
            board[choice] = 1
            if env_play.check_win(board) == 1:
                env_play.drawBoard(board)
                print('human win!')
                break

            if env_play.check_over(board):
                env_play.drawBoard(board)
                print('tie! game over!')
                break  

            action = model.choose_action(board, explore=False)
            null = [i for i in range(len(board)) if board[i] == 0]
            if action not in null:
                print('human win!')
                break
            board[action] = 2
            env_play.drawBoard(board)
            if env_play.check_win(board) == 2:
                env_play.drawBoard(board)
                print('AI win!')
                break
            
            if env_play.check_over(board):
                env_play.drawBoard(board)
                print('tie! game over!')
                break

    if mode == 'second':
        model.load_table('Q_table', 'Q_learn1')
        board = env_play.reset()
        env_play.drawBoard(board)
        while True:
            action = model.choose_action(board, explore=False)
            null = [i for i in range(len(board)) if board[i] == 0]
            if action not in null:
                print('human win!')
                break
            board[action] = 2
            env_play.drawBoard(board)
            if env_play.check_win(board) == 2:
                env_play.drawBoard(board)
                print('AI win!')
                break

            if env_play.check_over(board):
                env_play.drawBoard(board)
                print('tie! game over!')
                break  

            choice = human_input(board)
            board[choice] = 1
            if env_play.check_win(board) == 1:
                env_play.drawBoard(board)
                print('human win!')
                break
            
            if env_play.check_over(board):
                env_play.drawBoard(board)
                print('tie! game over!')
                break  

def human_input(board):
    while True:
        choice = int(input('please choice: '))
        assert 0 <= choice <=8 , 'please type 0 to 8'
        null = [i for i in range(len(board)) if board[i] == 0]
        if choice not in null:
            print('please choice again!')
        else:
            break

    return choice


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--algorithm', default='Q-learning')
    args = parser.parse_args()
    assert args.algorithm == 'Q-learning' or args.algorithm == 'Sarsa', 'Please type Q-learning or Sarsa'

    times = 5 # number of games you want to play
    train(args)
    for i in range(times):
        play(args) 