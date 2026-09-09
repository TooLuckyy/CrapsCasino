import numpy as np
from enum import Enum

#define game status
class Status(Enum):
    COME_OUT = 1
    POINT = 2
    WINNER = 3
    CRAP_OUT = 4
    SEVEN_OUT = 5
    


class CrapsGame:
    #initalize game state
    def __init__(self):
        self.point = None
        self.status = Status.COME_OUT
        
    #rolls 2 dice outputing a random val 1-6 while also return sum of both die
    def roll(self):
        die_1 = np.random.randint(1, 7)
        die_2 = np.random.randint(1, 7)
    
        return die_1, die_2, die_1 + die_2
    
    #process game sequence and updates game state and rolls
    def process_roll(self):
        #checks if player is allowed to roll and return None if not valid
        can_roll = self.check_status()
        if not can_roll:
            return None
            
        player_roll = self.roll()
        total       = player_roll[2]
        
        #if comeout roll, come out rules are applied
        if self.status == Status.COME_OUT:
            if total in [7,11]:
                self.status = Status.WINNER
                
            elif total in [2,3,12]:
                self.status = Status.CRAP_OUT
                
            else:
                self.status = Status.POINT
                self.point  = player_roll[2]
                
        #if rolling for point, point rules applied
        elif self.status == Status.POINT:
            if total == self.point:
                self.status = Status.WINNER
                
            elif total == 7:
                self.status = Status.SEVEN_OUT
        
        return player_roll
    
    #checks current game state and validates if player can roll
    def check_status(self):
        if self.status in [Status.WINNER, Status.CRAP_OUT, Status.SEVEN_OUT]:
            return False
        
        return True
        
        
        
def main():
    game = CrapsGame()
    
    result = game.process_roll()
     
    print(result)
    print(game.status)
    print(game.point)

main()