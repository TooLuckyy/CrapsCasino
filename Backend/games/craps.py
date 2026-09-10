import numpy as np
from enum import Enum

#define game status
class Status(Enum):
    COME_OUT = 1
    POINT = 2
    WINNER = 3
    CRAP_OUT = 4
    SEVEN_OUT = 5
    
#define bet sizes
class BetAmount(Enum):
    ONE = 1
    FIVE = 5
    TEN = 10
    TWENTY_FIVE = 25
    FIFTY = 50
    ONE_HUNDRED = 100

#define bet types
class BetType(Enum):
    PASS_LINE = "pass_line"
    DONT_PASS = "dont_pass"
    FIELD = "field"
    COME = "come"
    DONT_COME = "dont_come"
    PLACE_4 = "place_4"
    PLACE_5 = "place_5"
    PLACE_6 = "place_6"
    PLACE_8 = "place_8"
    PLACE_9 = "place_9"
    PLACE_10 = "place_10"
    PASS_ODDS = "pass_odds"
    DONT_PASS_ODDS = "dont_pass_odds"

#Enum of bet state
class BetStatus(Enum):
    OFF = "off"
    ON = "on"
    CLOSED = "closed"


class CrapsGame:
    #initalize game state
    def __init__(self):
        self.point = None
        self.status = Status.COME_OUT
        self.bets = []
        
    #rolls 2 dice outputing a random val 1-6 while also return sum of both die
    def roll(self):
        die_1 = np.random.randint(1, 7)
        die_2 = np.random.randint(1, 7)
    
        return die_1, die_2, die_1 + die_2
    
    #process game sequence and updates game state and rolls
    def process_roll(self):
        
        #checks if player is allowed to roll and return None if not valid
        if self.status in [Status.WINNER, Status.CRAP_OUT, Status.SEVEN_OUT]:
            return None
            
        player_roll = self.roll()
        total       = player_roll[2]
        
        #if comeout roll, come out rules are applied
        if self.status == Status.COME_OUT:
            if total in [7,11]:
                self.status = Status.WINNER
                
                for bet in self.bets:
                    if bet.bet_type == BetType.DONT_PASS:
                        self.lose_bet(bet)       #don't pass line bet is removed
                    
                    elif bet.bet_type == BetType.PASS_LINE:
                        self.pay_bet(bet)        #pass line bet is payed  
                    
                    elif bet.bet_type == BetType.FIELD:
                        if total == 7:
                            self.lose_bet(bet)   #field bet is lost
                        else:
                            self.pay_bet(bet)    #field bet is payed
                
            elif total in [2,3,12]:
                self.status = Status.CRAP_OUT
                
                for bet in self.bets:
                    if bet.bet_type == BetType.DONT_PASS:
                        self.pay_bet(bet)
                        
                    elif bet.bet_type == BetType.PASS_LINE:
                        self.lose_bet(bet)
                        
                    elif bet.bet_type == BetType.FIELD:
                        if total == 12:
                            self.push_bet(bet)
                        else:
                            self.pay_bet(bet)
                    
            else:
                self.status = Status.POINT
                self.point  = player_roll[2]
                
                for bet in self.bets:
                    if bet.bet_type == BetType.FIELD:
                        if total in [5,6,8]:
                            self.lose_bet(bet)
                        else:
                            self.pay_bet(bet)
                
        #if rolling for point, point rules applied
        elif self.status == Status.POINT:
            if total == self.point:
                self.status = Status.WINNER
                
            elif total == 7:
                self.status = Status.SEVEN_OUT
                
        return player_roll
    
    #adds a specified bet type and amount to a bets array
    def place_bet(self, bet_type, amount):
        #check if bet amount meets minimum requirements
        if amount < 10:
            return None
        
        bet = Bet(bet_type, amount)
        self.bets.append(bet)
    
    #def remove_bet(self):
    
    #pays the winners bet    
    #def pay_bet(self, bet):
    
    #takes the losing bets
    #def lose_bet(self, bet):
    
    #a tie bet/push users bet it returned
    #def pass_bet(self, bet):
        
    
class Bet:
    def __init__(self, bet_type, amount):
        self.bet_type = bet_type
        self.amount = amount
        self.status = BetStatus.ON
        self.number = None
    
    #switches bet status to on
    def turn_on(self):
        self.status = BetStatus.ON
    
    #switches bet status to off
    def turn_off(self):
        self.status = BetStatus.OFF
        
    #switches bet status to off
    def close(self):
        self.status = BetStatus.CLOSED
        
    #sets number attribut to specified number
    def set_number(self, num):
        self.number = num

        
def main():
    game = CrapsGame()
    
    result = game.process_roll()
     
    print(result)
    print(game.status)
    print(game.point)

main()