from random import random
from Card import *
from RoyalCard import *

class Dealer(object):
    def __init__(self) -> None:
        self.bet = 0
        self.over = False
        self.giveup = False
    def action(self, hands, public, minBet):
        self.hands=hands
        r = random.random()
        if len(public) == 0:
            if self.hands[0].point + self.hands[1].point >= 20:
                if r <= 0.7: self.Bet(minBet)
                else: self.Bet(2*minBet)
            elif self.hands[0].point == self.hands[1].point:
                if r <= 0.8: self.Bet(2*minBet)
                else: self.Bet(3*minBet)
            elif self.hands[0].point + self.hands[1].point <= 8:
                if r <= 0.4: self.fold()
                else: self.Bet(2*minBet)
            else:
                if r <= 0.2: self.fold()
                else: self.Bet(minBet)
        else:
            case = findMaxComb(public + self.hands)
            if CASELIST.index(case.case) <= CASELIST.index('Straight'):
                if r <= 0.9: self.Bet(3*minBet)
                elif r <= 0.95: self.Bet(4*minBet)
                else: self.Bet(10*minBet)

            elif case.case == 'Three':
                if r <= 0.7: self.Bet(2*minBet)
                elif r <= 0.9: self.Bet(3*minBet)
                else: self.Bet(minBet)
            elif case.case == 'Pairs':
                if r <= 0.1: self.fold()
                else: self.Bet(minBet)
            elif case.case == 'Pair':
                if r <= 0.2: self.fold()
                else: self.Bet(minBet)
            elif case.case == 'High':
                if r <= 0.5: self.fold()
                elif r <= 0.9: self.call(minBet)
                else: self.Bet(2*minBet)


    def call(self, bet:int):
        print('@@ BOT CALL')
        self.bet += (bet - self.bet)
        self.over = True
    def fold(self):
        print('@@ BOT FOLD')
        self.over = True
        self.giveup = True

    def minBet(self, bet:int):
        print('@@ BOT MINBET', bet)
        self.bet += bet

    def Bet(self, bet:int):
        print('@@ BOT BET', bet)
        self.bet += bet
            
    def allIn(self):
        self.bet += self.coin
        self.over = True