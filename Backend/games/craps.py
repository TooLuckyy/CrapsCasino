import numpy as np
from enum import Enum

#define game status
class Status(Enum):
    COME_OUT = 1
    POINT = 2
    WINNER = 3
    CRAP_OUT = 4
    


class CrapsGame:
    #initalize game state
    def __init__(self):
        self.point = None
        self.Status = Status.COME_OUT
        
    #rolls 2 dice outputing a random val 1-6 while also return sum of both die
    def roll(self):
        die1 = np.random.randint(1, 7)
        die2 = np.random.randint(1, 7)
    
        return die1, die2, die1 + die2
    
    def process_roll(self):
        player_roll = self.roll()
        
        if player_roll[2] in [7,11]:
            self.Status = Status.WINNER
        elif player_roll[2] in [2,3,12]:
            self.Status = Status.CRAP_OUT
        else:
            self.Status = Status.POINT
            self.point = player_roll[2]
        
        return player_roll
        
def main():
    game = CrapsGame()
    
    print(game.Status)
    print(game.point)
    print(game.roll())

main()