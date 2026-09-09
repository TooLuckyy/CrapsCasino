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
        self.status = Status.COME_OUT
        
    #rolls 2 dice outputing a random val 1-6 while also return sum of both die
    def roll(self):
        die1 = np.random.randint(1, 7)
        die2 = np.random.randint(1, 7)
    
        return die1, die2, die1 + die2
    
    #process game sequence and updates game state and rolls
    def process_roll(self):
        player_roll = self.roll()
        total = player_roll[2]
        
        #if comeout roll, come out rules are applied
        if self.status == Status.COME_OUT:
            if total in [7,11]:
                self.status = Status.WINNER
                
            elif total in [2,3,12]:
                self.status = Status.CRAP_OUT
                
            else:
                self.status = Status.POINT
                self.point = player_roll[2]
                
        #if rolling for point, point rules applied
        elif self.status == Status.POINT:
            if total == self.point:
                self.status = Status.WINNER
                
            elif total == 7:
                self.status = Status.CRAP_OUT
        
        
        
def main():
    game = CrapsGame()
    
    result = game.process_roll()
     
    print(result)
    print(game.status)
    print(game.point)

main()