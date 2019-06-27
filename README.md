# TicTac-RL
A RL based algorithm (Q-Learning&amp;Sarsa) for training an intelligent agent to play the tictac game uisng Python and Numpy
# Introduction
The reinforcement learning system is built as three parts:
- agent - the decision maker (`QLearn.py` and `Sarsa.py`)
- environment - the rule of tictac game (`tictac_env.py`)
- interactive interface - where training and testing are performed (`run_tictac_RL.py`) 
# Prerequisites
```
python 3.6
Numpy
```
# Usage
`python3 run_tictac_RL.py --algorithm Q-learning # or Sarsa`
# Reference
**Q-learning** and **Sarsa** are implemented as described in [Reinforcement Learning:
An Introduction](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf) (Chapter6, P154-P157)