# Class representing a hand of cards
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def clear(self):
        self.cards = []

    def value(self):
        value = 0
        ace_count = 0
        for card in self.cards:
            rank = card.split('_')[0]
            if rank in ['J', 'Q', 'K']:
                value += 10
            elif rank == 'A':
                ace_count += 1
                value += 11
            else:
                value += int(rank)

        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1

        return value

    def has_ace(self):
        return True if (self.cards.count('A_of_clubs') or self.cards.count('A_of_diamonds') or
                        self.cards.count('A_of_hearts') or self.cards.count('A_of_spades')) else False
