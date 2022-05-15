import random

_SUIT_ = ['Spade', 'Heart', 'Diamond', 'Club']
_POINT_ = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card(object):
    def __init__(self, suit:str, point:int) -> None:
        assert suit in _SUIT_
        assert point in list(range(2,15))
        self.suit = suit
        self.point = point
        self.name = suit + ' ' + _POINT_[point-2]
    def __lt__(self, other) -> bool:
        return self.point < other.point
    def __le__(self, other) -> bool:
        return self.point <= other.point 
    def __gt__(self, other) -> bool:
        return self.point > other.point
    def __ge__(self, other) -> bool:
        return self.point >= other.point
    def __eq__(self, other) -> bool:
        return self.point == other.point
    def __ne__(self, other) -> bool:
        return self.point != other.point
    def __str__(self) -> str:
        poke = \
''' ------
| {:s}   |
| {:s}    |
|      |
 ------'''.format(
    _POINT_[self.point-2] + ' 'if self.point!=10 else _POINT_[self.point-2],
    self.suit[0]
            )
        return poke

class Deck(object):
    def __init__(self) -> None:
        self.deck = [Card(suit, point) for suit in _SUIT_ for point in list(range(2,15))]

    def draw(self, num=1):
        ''' Args:
            * num: number of the cards to be drawn.
            Result:
            * Return a list of drawn cards
        '''
        if num > len(self): return -1
        return [self.deck.pop() for i in range(num)]

    def shuffle(self, rseed=0):
        ''' Args:
            * rseed: random seed for shuffle.
        '''
        random.seed(rseed)
        random.shuffle(self.deck)

    def __len__(self):
        return len(self.deck)