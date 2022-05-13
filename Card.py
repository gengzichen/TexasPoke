_SUIT_ = ['Spade', 'Heart', 'Diamond', 'Clube']
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

class Deck(object):
    def __init__(self) -> None:
        self.deck = [Card(suit, point) for suit in _SUIT_ for point in list(range(2,15))]
        self._len_ = 
    def 