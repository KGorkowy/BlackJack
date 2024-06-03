import copy
import random
import sys

import pygame

# Inicjalizacja Pygame
pygame.init()

# Zmienne globalne
cards_from_one_color = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards_from_one_color
decks_in_game = 4
WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Blackjack')
timer = pygame.time.Clock()
FPS = 60
pygame.font.init()
font = pygame.font.SysFont('Arial', 50)
title_font = pygame.font.SysFont('Arial', 100)
author_font = pygame.font.SysFont('Arial', 20)
balance_font = pygame.font.SysFont('Arial', 40)
active = False
initial_deal = False
game_deck = copy.deepcopy(one_deck * decks_in_game)
player_hand = []
dealer_hand = []
outcome = 0


# Kolory
green = (35, 144, 35)
darkgreen = (15, 62, 15)
black = (0, 0, 0)
white = (255, 255, 255)

# Wczytanie wzoru w tle
pattern = pygame.image.load('pattern.png').convert_alpha()
pattern = pygame.transform.scale(pattern, (WIDTH, HEIGHT))

# Funkcja do losowego wybierania karty z talii, jedna karta na raz
def deal_cards(hand, deck):
    card_index = random.randint(0, len(deck))
    hand.append(hand[card_index-1])
    deck.pop(card_index-1)
    print(hand, deck)

# Funkcja do rysowania tekstu
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    text_rect = textobj.get_rect()
    text_rect.center = (x, y)
    surface.blit(textobj, text_rect)


# Funkcja do rysowania tła z patternem
def draw_background():
    screen.fill(darkgreen)
    for y in range(0, HEIGHT, pattern.get_height()):
        for x in range(0, WIDTH, pattern.get_width()):
            screen.blit(pattern, (x, y))


# Funkcja do rysowania menu głównego
def draw_main_menu():
    while True:
        draw_background()
        draw_text("Blackjack", title_font, white, screen, WIDTH / 2, HEIGHT / 4)
        draw_text("Made by Kamil Górkowy", author_font, white, screen, WIDTH / 2, HEIGHT / 4 + 75)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        start_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100)
        exit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 100)

        pygame.draw.rect(screen, black, start_button)
        pygame.draw.rect(screen, black, exit_button)

        draw_text("Start", font, white, screen, start_button.centerx, start_button.centery)
        draw_text("Exit", font, white, screen, exit_button.centerx, exit_button.centery)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if click:
            if start_button.collidepoint((mouse_x, mouse_y)):
                game_loop()
            if exit_button.collidepoint((mouse_x, mouse_y)):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        timer.tick(FPS)


# Funkcja do rysowania gry
def draw_game(player_balance):
    button_list = []
    draw_background()
    if not active:
        deal_button = pygame.Rect(150, 20, 300, 100)
        pygame.draw.rect(screen, white, deal_button)
        pygame.draw.rect(screen, black, deal_button, 3)
        deal_text = font.render('Deal', True, black)
        deal_text_rect = deal_text.get_rect(center=deal_button.center)
        screen.blit(deal_text, deal_text_rect)
        button_list.append(deal_button)
    else:
        hit_button = pygame.Rect(0, 700, 300, 100)
        pygame.draw.rect(screen, white, hit_button)
        pygame.draw.rect(screen, black, hit_button, 3)
        hit_text = font.render('Hit', True, black)
        hit_text_rect = hit_text.get_rect(center=hit_button.center)
        screen.blit(hit_text, hit_text_rect)
        button_list.append(hit_button)

        stand_button = pygame.Rect(300, 700, 300, 100)
        pygame.draw.rect(screen, white, stand_button)
        pygame.draw.rect(screen, black, stand_button, 3)
        stand_text = font.render('Stand', True, black)
        stand_text_rect = stand_text.get_rect(center=stand_button.center)
        screen.blit(stand_text, stand_text_rect)
        button_list.append(stand_button)

    player_balance_display = pygame.Rect(800, 700, 300, 100)
    pygame.draw.rect(screen, white, player_balance_display)
    pygame.draw.rect(screen, black, player_balance_display, 3)
    player_balance_text_1 = balance_font.render('Your balance:', True, black)
    player_balance_text_2 = balance_font.render("%.2f$" % round(player_balance, 2), True, black)
    player_balance_text_1_rect = player_balance_text_1.get_rect(center=(player_balance_display.centerx, player_balance_display.centery - 20))
    player_balance_text_2_rect = player_balance_text_2.get_rect(center=(player_balance_display.centerx, player_balance_display.centery + 20))
    screen.blit(player_balance_text_1, player_balance_text_1_rect)
    screen.blit(player_balance_text_2, player_balance_text_2_rect)
    pygame.display.update()
    return button_list


# Pętla gry
def game_loop():
    global active, initial_deal, player_hand, dealer_hand, game_deck
    player_balance = 100.0
    run = True
    while run:
        # Początkowe rozdanie
        if initial_deal:
            for i in range(2):
                player_hand, game_deck = deal_cards(player_hand, game_deck)
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        buttons = draw_game(player_balance)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not active:
                    if buttons[0].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(one_deck * decks_in_game)
                        player_hand = []
                        dealer_hand = []
                        outcome = 0


        pygame.display.update()
        timer.tick(FPS)


if __name__ == "__main__":
    draw_main_menu()