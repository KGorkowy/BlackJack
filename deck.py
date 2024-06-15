import copy
import random

# Cards settings
cards_from_one_color = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['hearts', 'diamonds', 'clubs', 'spades']
one_deck = [f"{rank}_of_{suit}" for suit in suits for rank in cards_from_one_color]
decks_in_game = 4


# Class representing a deck of cards
class Deck:
    def __init__(self):
        self.deck = copy.deepcopy(one_deck * decks_in_game)
        random.shuffle(self.deck)

    def deal_card(self):
        if len(self.deck) == 0:
            raise ValueError("No more cards in the deck.")
        return self.deck.pop()
