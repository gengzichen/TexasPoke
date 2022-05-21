from regex import P
from Card import Deck
from Dealer import Dealer
from RoyalCard import *
from Player import *
import time


class Game(object):
    def __init__(self, PLAYER:Player, DEALER:Dealer) -> None:
        self.state_list = ['Pre','Blind', 'Flop', 'Turn', 'River']
        self.action_list = ['fold', 'call', 'minBet', 'bet', 'allIn', 'check']
        self.Player = PLAYER
        self.Dealer = DEALER
        self.PlayerCard = []
        self.DealerCard = []
        self.PublicCard = []
        self.Pot = 0
        self.end = False
        self.state = 'Blind'
        self.minBet = 10


        self.Deck = Deck()
        self.t = int(time.time())
        self.Deck.shuffle(self.t)
        self.Deck.shuffle(self.t)
        # Pre bet part, this part is fixed
        self.Player.Bet(10)
        self.Dealer.Bet(2*10)
        self.state = 'Blind'
        self.DealerCard = self.Deck.draw(2)
        self.PlayerCard = self.Deck.draw(2)
        self.result = 0

        self.actions = ['fold', 'call', 'minBet', 'allIn', 'bet']
    
    def feasible_action(self):

        if self.end:
            self.actions = []
        elif self.state == 'ShowHand':
            self.actions = ['check']
        # no coin has to give up
        elif self.Player.coin < self.minBet:
            self.actions = ['fold']
        # No fold or Call
        elif self.Player.bet == 0 and self.Dealer.bet == 0:
            self.actions = ['check', 'minBet', 'allIn', 'bet']
        # No check
        elif self.Player.bet != 0 or self.Dealer.bet != 0:
            self.actions = ['fold', 'call', 'minBet', 'allIn', 'bet']
    def give_up(self):
        # if dealer fold:
        self.result = self.Player.bet + self.Dealer.bet + self.Pot
        self.Player.coin += self.Player.bet + self.Dealer.bet + self.Pot
        self.Pot = 0
        self.Player.bet = 0
        self.Dealer.bet = 0
        self.Dealer.giveup = False
        self.end = True
        self.Player.over = False
        self.Dealer.over = False
        

    def play(self, action:str, bet:int):            
        if action == 'fold':
            self.result = -(self.Player.bet+self.Dealer.bet+self.Pot)
            self.Player.bet = 0
            self.Dealer.bet = 0
            self.end = True
            self.feasible_action()
            return False

        if self.state == 'Blind':
            # Bet not over, continue to add
            if not self.Dealer.over and not self.Player.over:
                self.Player.action(action, self.Dealer.bet, bet)
                self.minBet = max([self.Player.bet, self.Dealer.bet])
                if self.Player.over == False:
                    self.Dealer.action(self.DealerCard, self.PublicCard, max([10,self.minBet]))
                    # force bet to end if not enough money
                    if self.Player.coin < self.Dealer.bet:
                        self.Dealer.call(self.Player.bet)
                else:
                    self.Dealer.message = ''

                self.minBet = max([self.Player.bet, self.Dealer.bet])
                if self.Dealer.giveup: 
                    self.give_up()
                    return False

            # Bet over, put bets into pot
            if self.Dealer.over or self.Player.over:
                self.Pot = self.Player.bet + self.Dealer.bet + self.Pot
                self.Dealer.bet = 0
                self.Player.bet = 0
                self.minBet = 10

                if len(self.PublicCard)==0:
                    self.PublicCard = self.Deck.draw(3)
                self.state = 'Flop'
                self.Dealer.over = False
                self.Player.over = False
            self.feasible_action()
            if self.Player.coin < self.minBet or self.Player.coin == 0:
                self.state = 'ShowHand'
                self.actions = ['check']


        elif self.state == 'Flop':
            # Bet not over, continue to add
            if not self.Dealer.over and not self.Player.over:
                self.Player.action(action, self.Dealer.bet, bet)
                self.minBet = max([self.Player.bet, self.Dealer.bet])
                if self.Player.over == False:
                    self.Dealer.action(self.DealerCard, self.PublicCard, max([10,self.minBet]))
                    # force bet to end if not enough money
                    if self.Player.coin < self.Dealer.bet:
                        self.Dealer.call(self.Player.bet)
                else:
                    self.Dealer.message = ''

                self.minBet = max([self.Player.bet, self.Dealer.bet])
                if self.Dealer.giveup: 
                    self.give_up()
                    return False

            # Bet over, put bets into pot
            if self.Dealer.over or self.Player.over:
                self.Pot = self.Player.bet + self.Dealer.bet + self.Pot
                self.Dealer.bet = 0
                self.Player.bet = 0
                self.minBet = 10

                if len(self.PublicCard)==3:
                    self.PublicCard += self.Deck.draw(1)
                self.state = 'Turn'
                self.Dealer.over = False
                self.Player.over = False
            self.feasible_action()
            if self.Player.coin < self.minBet or self.Player.coin == 0:
                self.state = 'ShowHand'
                self.actions = ['check']

        elif self.state == 'Turn':
            # Bet not over, continue to add
            if not self.Dealer.over and not self.Player.over:
                self.Player.action(action, self.Dealer.bet, bet)
                self.minBet = max([self.Player.bet, self.Dealer.bet])
                if self.Player.over == False:
                    self.Dealer.action(self.DealerCard, self.PublicCard, max([10,self.minBet]))
                    # force bet to end if not enough money
                    if self.Player.coin < self.Dealer.bet:
                        self.Dealer.call(self.Player.bet)
                else:
                    self.Dealer.message = ''

                self.minBet = max([self.Player.bet, self.Dealer.bet])
                if self.Dealer.giveup: 
                    self.give_up()
                    return False

            # Bet over, put bets into pot
            if self.Dealer.over or self.Player.over:
                self.Pot = self.Player.bet + self.Dealer.bet + self.Pot
                self.Dealer.bet = 0
                self.Player.bet = 0
                self.minBet = 10

                if len(self.PublicCard)==4:
                    self.PublicCard += self.Deck.draw(1)
                self.state = 'River'
                self.Dealer.over = False
                self.Player.over = False
            self.feasible_action()
            if self.Player.coin < self.minBet or self.Player.coin == 0:
                self.state = 'ShowHand'
                self.actions = ['check']

        elif self.state == 'River':
            # Bet not over, continue to add
            if not self.Dealer.over and not self.Player.over:
                self.Player.action(action, self.Dealer.bet, bet)
                self.minBet = max([self.Player.bet, self.Dealer.bet])
                if self.Player.over == False:
                    self.Dealer.action(self.DealerCard, self.PublicCard, max([10,self.minBet]))
                    # force bet to end if not enough money
                    if self.Player.coin < self.Dealer.bet:
                        self.Dealer.call(self.Player.bet)
                else:
                    self.Dealer.message = ''

                self.minBet = max([self.Player.bet, self.Dealer.bet])
                if self.Dealer.giveup: 
                    self.give_up()
                    return False

            # Bet over, put bets into pot
            if self.Dealer.over or self.Player.over:
                self.Pot = self.Player.bet + self.Dealer.bet + self.Pot
                self.Dealer.bet = 0
                self.Player.bet = 0
                self.minBet = 10

                self.state = 'ShowHand'
                self.Dealer.over = False
                self.Player.over = False
            self.feasible_action()
            if self.Player.coin < self.minBet or self.Player.coin == 0:
                self.state = 'ShowHand'
                self.actions = ['check']

        elif self.state == 'ShowHand':
            if len(self.PublicCard) < 5:
                self.PublicCard += self.Deck.draw(5-len(self.PublicCard))

            PlayerCase = findMaxComb(self.PlayerCard + self.PublicCard)
            DealerCase = findMaxComb(self.DealerCard + self.PublicCard)
            if PlayerCase > DealerCase:
                self.result = self.Pot
                self.Player.coin += self.Pot
            elif PlayerCase < DealerCase:
                self.result = -self.Pot
            else:
                self.Player.coin += self.Pot / 2
            self.Pot = 0

            self.end = True
            self.actions = []

        else:
            return None



        
Zen = UserAccount('Zen', 'gengzichenchin@gmail.com', 2000)

def main():
    # After Login, start initialize the player and dealer
    PLAYER = Zen.newPlayer()
    DEALER = Dealer()



def getUser():
    # Get user from data base, return a user. 
    pass
