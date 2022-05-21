from Game import *
from Player import *
from Dealer import * 
from Card import *
from RoyalCard import *

Zen = UserAccount('Zen', 'gengzichenchin@gmail.com', 2000)
Player = Zen.newPlayer()
Dealer = Dealer()
mygame = Game(Player, Dealer)

print('Welcome to the Royal Card Game')
print('-'*50)

while(mygame.end==False):
    print('='*60)
    print('Your coin:', mygame.Player.coin)
    print('POT:', mygame.Pot)
    print('Dealer Card:', ['unknown', 'unknown'], 'Dealer Bet:', mygame.Dealer.bet)
    if len(mygame.PublicCard) != 0:
        print('Plublic Card:', [card.name for card in mygame.PublicCard])
    print('Your Card:', [card.name for card in mygame.PlayerCard], 'Player Bet:', mygame.Player.bet)
    print('='*60)
    print('You can', [i for i in mygame.actions])
    input_action = input('Input your action:')
    input_action = input_action.split(' ')
    act = ''
    bet = 0
    while input_action[0] not in mygame.actions:
        print('You can', [i for i in mygame.actions])
        input_action = input('Input your action:')
        input_action = input_action.split(' ')
    act = input_action[0]
    if len(input_action) > 1:
        bet = int(input_action[1])
    mygame.play(action=act, bet = bet)
    if mygame.Player.message != '': print( mygame.Player.message)
    if mygame.Dealer.message != '': print( mygame.Dealer.message)

print('='*60)
print('Your coin:', mygame.Player.coin)
print('POT:', mygame.Pot)
print('Dealer Card:', [card.name for card in mygame.DealerCard], 'Dealer Bet:', mygame.Dealer.bet)
if len(mygame.PublicCard) != 0:
    print('Plublic Card:', [card.name for card in mygame.PublicCard])
print('Your Card:', [card.name for card in mygame.PlayerCard], 'Player Bet:', mygame.Player.bet)
print('='*60)

print('Game over!', 'You won' if mygame.result >=0 else 'You lost', abs(mygame.result))


