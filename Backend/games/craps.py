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
                self.status = Status.CRAP_OUT    #switch game status to crap out
                
                #checks for active bets and updates
                for bet in self.bets:
                    if bet.bet_type == BetType.DONT_PASS:
                        self.pay_bet(bet)
                        
                    elif bet.bet_type == BetType.PASS_LINE:
                        self.lose_bet(bet)
                        
                    elif bet.bet_type == BetType.FIELD:
                        if total == 12:
                            self.push_bet(bet)    #bet is tied and returned
                        else:
                            self.pay_bet(bet)
                    
            else:
                self.status = Status.POINT
                self.point  = total
                                
                
        #when rolling for point pass line rules are applied and bets are updated
        elif self.status == Status.POINT:
            
            #determine the outcome of the current round
            if total == 7:
                self.status = Status.SEVEN_OUT #sets status to seven out
                
            elif total == self.point:
                self.status = Status.WINNER    #sets status to winner
            
            #checks active bets and applies betting rules for that object
            for bet in self.bets:
                match bet.bet_type: 
                    #match each bet to its bet type and pays or losses are applied
                    case BetType.PASS_LINE:
                        if total == 7:
                            self.lose_bet(bet)
                            
                        elif total == self.point:
                            self.pay_bet(bet)
                        
                    case BetType.DONT_PASS: 
                        if total == self.point:
                            self.lose_bet(bet)
                            
                        elif total == 7:
                            self.pay_bet(bet)
                        
                    case BetType.FIELD: #field logic is checked
                        if total in [5,6,7,8]:
                            self.lose_bet(bet)
                        else:
                            self.pay_bet(bet)
                            
                    case BetType.COME: #come bet logic is checked
                        if bet.number == None:
                            if total in [7,11]:
                                self.pay_bet(bet)
                                
                            elif total in [2,3,12]:
                                self.lose_bet(bet)
                                
                            else:
                                bet.set_number(total) #if no come bet number is established, establish one
                                
                        else:
                            if total == 7:
                                self.lose_bet(bet)
                            elif total == bet.number:
                                self.pay_bet(bet)
                                
                    case BetType.DONT_COME: #come bet logic is checked
                        if bet.number == None:
                            if total in [7,11]:
                                self.lose_bet(bet)
                                
                            elif total in [2,3]:
                                self.pay_bet(bet)
                                
                            elif total == 12:
                                self.push_bet(bet)
                            
                            else:
                                bet.set_number(total) #if no active come bet set come bet number
                        
                        else:
                            if total == 7:
                                self.pay_bet(bet)
                            elif total == bet.number:
                                self.lose_bet(bet)
                    
                    #place bets are checked and bet rules are applied            
                    case BetType.PLACE_4 | BetType.PLACE_5 | BetType.PLACE_6 | BetType.PLACE_8 | BetType.PLACE_9 | BetType.PLACE_10 as place_bet:
                        place_number = int(place_bet.value.split("_")[1]) #typecase the enum value of place bet (a string) into its number
                        
                        if place_number == total:
                            self.pay_bet(bet)
                        elif total == 7:
                            self.lose_bet(bet)
                    
                    #odds bets win on pass line or don't pass line rules        
                    case BetType.PASS_ODDS:
                        if total == 7:
                            self.lose_bet(bet)
                        elif total == self.point:
                            self.pay_bet(bet)
                            
                    case BetType.DONT_PASS_ODDS:
                        if total == 7:
                            self.pay_bet(bet)
                        elif total == self.point:
                            self.lose_bet(bet)
                                     
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
    #def push_bet(self, bet):
        
    
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
    
    game.place_bet("pass_line", 10)
    
    result = game.process_roll()
     
    print(result)
    print(game.status)
    print(game.point)
    
    game.roll()
    result2 = game.process_roll()
    
    print(result2)
    print(game.status)
    print(game.point)

main()