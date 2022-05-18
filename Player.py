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
        print('@@ user call', (bet - self.bet))
        self.coin -= (bet - self.bet)
        self.bet += (bet - self.bet)
        self.over = True
    def fold(self):
        self.over = True
    def minBet(self, bet):
        print('HERERE')
        if bet == 0: bet = 10
        self.coin -= bet
        self.bet += bet
    def Bet(self, bet):
        print('@@ user bet', bet)
        self.coin -= bet
        self.bet += bet
    def allIn(self):
        self.coin = 0
        self.bet += self.coin
        self.over = True