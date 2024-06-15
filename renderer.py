import pygame

# Window variables
WIDTH = 1200
HEIGHT = 900
FPS = 60
# Colors
green = (35, 144, 35)
darkgreen = (15, 62, 15)
black = (0, 0, 0)
white = (255, 255, 255)


# Class to render screen
class Renderer:
    def __init__(self, screen, resources):
        self.screen = screen
        self.resources = resources

    def draw_background(self):
        self.screen.fill(darkgreen)
        for y in range(0, HEIGHT, self.resources.pattern.get_height()):
            for x in range(0, WIDTH, self.resources.pattern.get_width()):
                self.screen.blit(self.resources.pattern, (x, y))

    def draw_text(self, text, font, color, x, y):
        textobj = font.render(text, True, color)
        text_rect = textobj.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(textobj, text_rect)

    def draw_cards(self, player_hand, dealer_hand, reveal_dealer_hand):
        # Drawing player's cards
        for i, card in enumerate(player_hand.cards):
            self.screen.blit(self.resources.card_images[card], (70 + (40 * i), 460))

        # Drawing dealer's cards
        for i, card in enumerate(dealer_hand.cards):
            if i == 0 or reveal_dealer_hand:
                # First dealer's card is shown, the rest are hidden
                self.screen.blit(self.resources.card_images[card], (70 + (40 * i), 150))
            else:
                self.screen.blit(self.resources.back_card_image, (70 + (40 * i), 150))

    def draw_main_menu(self):
        self.draw_background()
        self.draw_text("Blackjack", self.resources.title_font, white, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Made by Kamil Górkowy", self.resources.author_font, white, WIDTH / 2, HEIGHT / 4 + 75)

        start_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100)
        exit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 100)

        pygame.draw.rect(self.screen, black, start_button)
        pygame.draw.rect(self.screen, black, exit_button)

        self.draw_text("Start", self.resources.font, white, start_button.centerx, start_button.centery)
        self.draw_text("Exit", self.resources.font, white, exit_button.centerx, exit_button.centery)

        return start_button, exit_button

    def draw_dealer_score(self, dealer_score, show_dealer_score):
        dealer_score_text = self.resources.score_font.render(f'Dealer Score: {dealer_score if show_dealer_score else '###'}', True, white)
        self.screen.blit(dealer_score_text, (650, 300))

    def draw_game(self, player_balance, player_score, dealer_score, active, buttons, show_dealer_score, level, level_requirement):
        self.draw_background()
        if not active:
            deal_button = pygame.Rect(150, 20, 300, 100)
            pygame.draw.rect(self.screen, white, deal_button)
            pygame.draw.rect(self.screen, black, deal_button, 3)
            deal_text = self.resources.font.render('Deal', True, black)
            deal_text_rect = deal_text.get_rect(center=deal_button.center)
            self.screen.blit(deal_text, deal_text_rect)
            buttons.append(deal_button)
        else:
            hit_button = pygame.Rect(100, 750, 300, 100)
            pygame.draw.rect(self.screen, white, hit_button)
            pygame.draw.rect(self.screen, black, hit_button, 3)
            hit_text = self.resources.font.render('Hit', True, black)
            hit_text_rect = hit_text.get_rect(center=hit_button.center)
            self.screen.blit(hit_text, hit_text_rect)
            buttons.append(hit_button)

            stand_button = pygame.Rect(400, 750, 300, 100)
            pygame.draw.rect(self.screen, white, stand_button)
            pygame.draw.rect(self.screen, black, stand_button, 3)
            stand_text = self.resources.font.render('Stand', True, black)
            stand_text_rect = stand_text.get_rect(center=stand_button.center)
            self.screen.blit(stand_text, stand_text_rect)
            buttons.append(stand_button)

        player_balance_display = pygame.Rect(800, 750, 300, 100)
        pygame.draw.rect(self.screen, white, player_balance_display)
        pygame.draw.rect(self.screen, black, player_balance_display, 3)
        player_balance_text_1 = self.resources.balance_font.render('Your balance:', True, black)
        player_balance_text_2 = self.resources.balance_font.render("%.2f$" % round(player_balance, 2), True, black)
        player_balance_text_1_rect = player_balance_text_1.get_rect(
            center=(player_balance_display.centerx, player_balance_display.centery - 20))
        player_balance_text_2_rect = player_balance_text_2.get_rect(
            center=(player_balance_display.centerx, player_balance_display.centery + 20))
        self.screen.blit(player_balance_text_1, player_balance_text_1_rect)
        self.screen.blit(player_balance_text_2, player_balance_text_2_rect)

        # Displaying player and dealer scores
        player_score_text = self.resources.score_font.render(f'Player Score: {player_score}', True, white)
        self.screen.blit(player_score_text, (650, 600))
        self.draw_dealer_score(dealer_score, show_dealer_score)

        for i in range(10):
            self.screen.blit(self.resources.back_card_image, (3 * WIDTH // 4 + 20 - 2 * i, 150 + 10 - i))

        # Draw level and level requirements
        level_text = self.resources.score_font.render(f'Level: {level}', True, white)
        level_requirement_text = self.resources.score_font.render(f'Win Amount: {level_requirement}$', True, white)
        self.screen.blit(level_text, (WIDTH - 300, 20))
        self.screen.blit(level_requirement_text, (WIDTH - 300, 50))

    def draw_win_screen(self, player_balance, is_game_won=False):
        self.draw_background()
        self.draw_text(f"You reached ${player_balance}!", self.resources.title_font, white, WIDTH / 2, HEIGHT / 3)
        if is_game_won:
            self.draw_text("You completed all levels!", self.resources.title_font, white, WIDTH / 2, HEIGHT / 2)
        else:
            self.draw_text("Press 'Enter' to continue or 'ESC' to return to menu", self.resources.font, white, WIDTH / 2, HEIGHT / 2)
        pygame.display.update()

    def draw_loss_screen(self):
        self.draw_background()
        self.draw_text("You lost all your money!", self.resources.title_font, white, WIDTH / 2, HEIGHT / 3)
        self.draw_text("Press 'ESC' to return to menu", self.resources.font, white, WIDTH / 2, HEIGHT / 2)
        pygame.display.update()

    def draw_deck_empty_screen(self):
        self.draw_background()
        self.draw_text("The deck is empty!", self.resources.title_font, white, WIDTH / 2, HEIGHT / 3)
        self.draw_text("Press 'Y' to reshuffle or 'ESC' to return to menu", self.resources.font, white, WIDTH / 2,
                       HEIGHT / 2)
        pygame.display.update()
