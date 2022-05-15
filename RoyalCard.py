from itertools import combinations

CASELIST=['Royal Flush', 'Straight Flush', 'Four', 'Full House', 
          'Flush', 'Straight', 'Three', 'Pairs', 'Pair', 'High']

class Case(object):
    def __init__(self, hand) -> None:
        '''Args:
            * hand: a list of 5 cards.
        '''
        assert len(hand) == 5
        self.hand = hand
        self.case = 'High'
        self.kicker = sorted([card.point for card in hand])
        self.value = max(hand).point
        ''' The comparison will be performed by 
            1. First compare the case.
            2. If case is the same then will compare the kicker.
            3. If kicker is the same then the Case will be equal.
        '''
        self._get_case_()
        self.kicker_value = self._calc_kicker_()

    def _get_case_(self):
        hand_points = [card.point for card in self.hand]
        hand_freq = [hand_points.count(i) for i in hand_points]
        # Check for Four
        if max(hand_freq) == 4: 
            self.case = 'Four'
            self.value = hand_points[hand_freq.index(max(hand_freq))]
            self.kicker = []
            for p in hand_points: 
                if p != self.value: self.kicker.append(p)
        # Check for Full house
        if max(hand_freq) == 3 and _get_secmax_(hand_freq) == 2:
            self.case = 'Full House'
            self.value = hand_points[hand_freq.index(max(hand_freq))]
            self.kicker = []
            for p in hand_points: 
                if p != self.value: self.kicker.append(p)
        # Check for Three
        elif max(hand_freq) == 3 and _get_secmax_(hand_freq) == 1:
            self.case = 'Three'
            self.value = hand_points[hand_freq.index(max(hand_freq))]
            self.kicker = []
            for p in hand_points: 
                if p != self.value: self.kicker.append(p)
            self.kicker = sorted(self.kicker)
        # Check for Pairs
        elif max(hand_freq) == 2 and hand_freq.count(2) == 4:
            self.case = 'Pairs'
            pairs_points = []
            for p in hand_points:
                if hand_points.count(p) == 2:
                    pairs_points.append(p)
            pairs_points = sorted(list(set(pairs_points)))
            self.value = max(pairs_points)
            self.kicker = []
            for p in hand_points:
                if p != self.value and p not in self.kicker and p != pairs_points[0]: 
                    self.kicker.append(p)
            self.kicker.append(pairs_points[0])
                
        # Check for Pair
        elif max(hand_freq) == 2 and _get_secmax_(hand_freq) == 1:
            self.case = 'Pair'
            self.value = hand_points[hand_freq.index(max(hand_freq))]
            self.kicker = []
            for p in hand_points: 
                if p != self.value: self.kicker.append(p)
            self.kicker = sorted(self.kicker)

        # Check for Straight and Flush
        if self._isStraight_(hand_points):
            self.case = 'Straight'
            self.kicker = [max(hand_points)]
        if self._isFlush_():
            self.case = 'Flush'
            self.kicker = [max(hand_points)]
        if self._isFlush_() and self._isStraight_(hand_points):
            self.case = 'Straight Flush'
            self.kicker = [max(hand_points)]

    def _isStraight_(self, hand_points):
        minimum = min(hand_points)
        if sorted(hand_points) == list(range(minimum, minimum+5)):
            return True 
        else: return False

    def _isFlush_(self):
        hand_suits = [card.suit for card in self.hand]
        if len(set(hand_suits)) == 1: return True 
        else: return False
    
    def _calc_kicker_(self):
        result = 0
        for i in range(len(self.kicker)):
            result += (20**i) * self.kicker[i]
        return result


    def __lt__(self, other) -> bool:
        if CASELIST.index(self.case) > CASELIST.index(other.case): return True
        elif CASELIST.index(self.case) < CASELIST.index(other.case): return False
        elif self.case == other.case and self.value < other.value: return True
        elif self.value == other.value and self.kicker_value < other.kicker_value: return True
        else: return False

    def __le__(self, other) -> bool:
        return  self < other or self == other

    def __gt__(self, other) -> bool:
        if CASELIST.index(self.case) < CASELIST.index(other.case): return True
        elif CASELIST.index(self.case) > CASELIST.index(other.case): return False
        elif self.case == other.case and self.value > other.value: return True
        elif self.value == other.value and self.kicker_value > other.kicker_value: return True
        else: return False

    def __ge__(self, other) -> bool:
        return  self > other or self == other

    def __eq__(self, other) -> bool:
        return self.case == self.case and self.kicker_value == other.kicker_value

    def __ne__(self, other) -> bool:
        return self.case != self.case or self.kicker_value != other.kicker_value


def findMaxComb(Cards):
    assert len(Cards) >= 5
    combIndex = combinations(list(range(len(Cards))), 5)
    maxComb = None
    for idx in combIndex:
        tmpList = []
        for i in idx:
            tmpList.append(Cards[i])
        tmpCase = Case(tmpList)
        if maxComb is None:
            maxComb = tmpCase
        else: 
            #print(maxComb.case, maxComb.value, maxComb.kicker, maxComb.kicker_value)
            #print(tmpCase.case, tmpCase.value, tmpCase.kicker, tmpCase.kicker_value)
            maxComb = max([tmpCase, maxComb])
            #print('=='*30)
            #print(maxComb.case, maxComb.value, maxComb.kicker, maxComb.kicker_value)
            #print('=='*30)
    return maxComb

def _get_secmax_(lst):
    lst = list(set(lst))
    return sorted(lst)[-2]
