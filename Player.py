class UserAccount(object):
    def __init__(self, name, email, coin=1000) -> None:
        self.name = name
        self.email = email
        self.coin = coin
    def newPlayer(self):
        return Player(self.coin)


class Player(object):
    def __init__(self, coin) -> None:
        self.coin = coin
        self.bet = 0
        self.over = False
        self.message = ''
    def action(self, act:str, minBet:int, bet:int):
        if act == 'call': self.call(minBet)
        if act == 'check': self.check()
        if act == 'fold': self.fold()
        if act == 'minBet': self.minBet(minBet)
        if act == 'bet': self.Bet(bet)
        if act == 'allIn': self.allIn()

    def check(self):
        pass
    def call(self, bet:int):
        self.message = 'You called'
        self.coin -= (bet - self.bet)
        self.bet += (bet - self.bet)
        self.over = True
    def fold(self):
        self.message = 'You folded, dealer won'
        self.over = True
    def minBet(self, bet):
        self.message = 'You bet ' + str(bet)
        if bet == 0: bet = 10
        self.coin -= bet
        self.bet += bet
    def Bet(self, bet):
        self.message = 'You bet ' + str(bet)
        self.coin -= bet
        self.bet += bet
    def allIn(self):
        self.message = 'You put all in! No way back!'
        self.bet += self.coin
        self.coin = 0
