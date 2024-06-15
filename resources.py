import pygame

# Cards settings
cards_from_one_color = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['hearts', 'diamonds', 'clubs', 'spades']
one_deck = [f"{rank}_of_{suit}" for suit in suits for rank in cards_from_one_color]
decks_in_game = 4
WIDTH = 1200
HEIGHT = 900


# Class gathering resources used in the game
class Resources:
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 50)
        self.title_font = pygame.font.SysFont('Arial', 100)
        self.author_font = pygame.font.SysFont('Arial', 20)
        self.balance_font = pygame.font.SysFont('Arial', 40)
        self.score_font = pygame.font.SysFont('Arial', 30)
        self.pattern = pygame.image.load('pattern.png').convert_alpha()
        self.pattern = pygame.transform.scale(self.pattern, (WIDTH, HEIGHT))
        self.card_images = self.load_card_images()
        self.back_card_image = pygame.transform.scale(pygame.image.load('cards/back.png').convert_alpha(), (150, 210))
        self.card_shuffle_sound = pygame.mixer.Sound('sounds/card_shuffle.wav')
        self.card_take = pygame.mixer.Sound('sounds/card_take.wav')
        self.card_place = pygame.mixer.Sound('sounds/card_place.wav')
        self.chip_sound = pygame.mixer.Sound('sounds/chip.wav')
        self.fail_sound = pygame.mixer.Sound('sounds/fail.mp3')
        self.clap_sound = pygame.mixer.Sound('sounds/clap.mp3')

    def load_card_images(self, width=150, height=210):
        card_images = {}
        for card in one_deck:
            try:
                card_images[card] = pygame.transform.scale(pygame.image.load(f"cards/{card}.png").convert_alpha(),
                                                           (width, height))
            except pygame.error as e:
                print(f"Error loading image for card {card}: {e}")
        return card_images
