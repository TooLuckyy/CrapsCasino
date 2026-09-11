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
                            self.pay_bet(bet, total)    #field bet is payed
                
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
                            self.pay_bet(bet, total)
                    
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
                            self.pay_bet(bet, total)
                            
                    case BetType.COME: #come bet logic is checked
                        if bet.number is None:
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
                        if bet.number is None:
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
        
        #validate bet action
        match bet_type:
            #checks current game status to status bet is allowed
            case BetType.PASS_LINE:
                if self.status != Status.COME_OUT:
                    return None
                
            case BetType.DONT_PASS:
                if self.status != Status.COME_OUT:
                    return None
                
            case BetType.FIELD:
                if self.status not in [Status.POINT, Status.COME_OUT]:
                    return None
                
            case BetType.COME:
                if self.status != Status.POINT:
                    return None
                
            case BetType.DONT_COME:
                if self.status != Status.POINT:
                    return None
                
            case BetType.PLACE_4 | BetType.PLACE_5 | BetType.PLACE_6 | BetType.PLACE_8 | BetType.PLACE_9 | BetType.PLACE_10:
                if self.status != Status.POINT:
                    return None
                
            case BetType.PASS_ODDS:
                if self.status != Status.POINT:
                    return None
                
            case BetType.DONT_PASS_ODDS:
                if self.status != Status.POINT:
                    return None
        
        #for pass and don't pass odds validate and set number/bet its attached to if not just create the bet
        if bet_type == BetType.PASS_ODDS:
            valid = False
            
            #checks active bets for existing pass line bet 
            for bet in  self.bets:
                if bet.bet_type == BetType.PASS_LINE:
                    valid = True
                    break
                
            if not valid:
                return None
            
            #if bet found checks if odds bet already exist and denys re-bet
            for bet in self.bets:
                if bet.bet_type == BetType.PASS_ODDS:
                    return None
                
            bet = Bet(bet_type, amount, self.point)
        elif bet_type == BetType.DONT_PASS_ODDS:
            valid = False
            
            #checks if don't pass bet exist
            for bet in  self.bets:
                if bet.bet_type == BetType.DONT_PASS:
                    valid = True
                    break
                
            if not valid:
                return None

            #if bet found checks if there's already an active odds bet and denys re-bet
            for bet in self.bets:
                if bet.bet_type == BetType.DONT_PASS_ODDS:
                    return None
                
            bet = Bet(bet_type, amount, self.point)
            
        else:
            bet = Bet(bet_type, amount)

        self.bets.append(bet)
    
    #def remove_bet(self,bet_type, amount):
    
    #pays the winners bet    
    def pay_bet(self, bet, total = None):
        winnings = 0
        total_return = 0
        
        #match the bet type to its rule set and resolve bet
        match bet.bet_type:
            case BetType.PASS_LINE:
                winnings += bet.amount
                bet.close()
                
            case BetType.DONT_PASS:
                winnings += bet.amount
                bet.close()
            
            case BetType.FIELD:
                if total in [2,12]:
                    winnings += 2 * bet.amount
                else:
                    winnings += bet.amount
                bet.close()
                
            case BetType.COME:
                winnings += bet.amount
                bet.close()

            case BetType.DONT_COME:
                winnings += bet.amount
                bet.close()
                
            case BetType.PLACE_4 | BetType.PLACE_5 | BetType.PLACE_6 | BetType.PLACE_8 | BetType.PLACE_9 | BetType.PLACE_10 as place_bet:
                place_number = int(place_bet.value.split("_")[1]) #typecase the enum value of place bet (a string) into its number
                        
                match place_number:
                    case 4:
                        winnings += (9 * bet.amount) / 5
                    case 5:
                        winnings += (7 * bet.amount) / 5
                    case 6:
                        winnings += (7 * bet.amount) / 6
                    case 8:
                        winnings += (7 * bet.amount) / 6
                    case 9:
                        winnings += (7 * bet.amount) / 5
                    case 10:
                        winnings += (9 * bet.amount) / 5
            case BetType.PASS_ODDS:
                match bet.number:
                    case 4:
                        winnings += (2 * bet.amount)
                    case 5:
                        winnings += (3 * bet.amount) / 2
                    case 6:
                        winnings += (6 * bet.amount) / 5
                    case 8:
                        winnings += (6 * bet.amount) / 5
                    case 9:
                        winnings += (3 * bet.amount) / 2
                    case 10:
                        winnings += (2*bet.amount)
                        
                bet.close()
                
            case BetType.DONT_PASS_ODDS:
                match bet.number:
                    case 4:
                        winnings += (bet.amount) / 2
                    case 5:
                        winnings += (2 * bet.amount) / 3
                    case 6:
                        winnings += (5 * bet.amount) / 6
                    case 8:
                        winnings += (5 * bet.amount) / 6
                    case 9:
                        winnings += (2 * bet.amount) / 3
                    case 10:
                        winnings += (bet.amount) / 2
                        
                bet.close()
                
        total_return = winnings + bet.amount
        return winnings, total_return 
                
    
    #takes the losing bets
    def lose_bet(self, bet):
        bet.close()
    
    #a tie bet/push users bet it returned
    def push_bet(self, bet):
        bet.close()
        return bet.amount
        
    
class Bet:
    def __init__(self, bet_type, amount, number = None):
        self.bet_type = bet_type
        self.amount = amount
        self.status = BetStatus.ON
        self.number = number
    
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
    roll = 0
    game.place_bet(BetType.PASS_LINE, 10)
    
    result = game.process_roll()
     
    print(result)
    print(game.status)
    print(game.point)
    
    while roll == 0:
        roll = int(input("Roll again: "))
        
        result1 = game.process_roll()
        
        print(result1)
        print(game.status)
        print(game.point)
        
    return 0
    
    
main()