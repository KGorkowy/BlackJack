import sys
import pygame
import deck
import hand
import renderer
import resources

# Pygame initialization
pygame.init()

# Screen variables
WIDTH = 1200
HEIGHT = 900
FPS = 60

# Colors
green = (35, 144, 35)
darkgreen = (15, 62, 15)
black = (0, 0, 0)
white = (255, 255, 255)


# Main game class
class BlackjackGame:
    def __init__(self):
        pygame.display.set_caption('Blackjack')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.timer = pygame.time.Clock()
        self.resources = resources.Resources()
        self.renderer = renderer.Renderer(self.screen, self.resources)
        self.player_hand = hand.Hand()
        self.dealer_hand = hand.Hand()
        self.deck = deck.Deck()
        self.active = False
        self.initial_deal = False
        self.reveal_dealer_hand = False
        self.player_balance = 100.0
        self.win = False
        self.game_started = False
        self.round_result_checked = False
        self.level = 1
        self.level_requirements = {1: 120, 2: 150, 3: 200}
        self.level_up = False
        self.new_level = False

    def deal_initial_cards(self):
        self.player_hand.clear()
        self.dealer_hand.clear()
        for _ in range(2):
            self.animate_card_deal(self.player_hand, self.deck.deal_card())
            self.animate_card_deal(self.dealer_hand, self.deck.deal_card(), reveal=False)

    def animate_card_deal(self, hand, card, reveal=True):
        start_pos = (3 * WIDTH // 4, 150)
        target_y = 450 if hand == self.player_hand else 150
        end_pos = (70 + 40 * len(hand.cards), target_y)
        card_image = self.resources.back_card_image if (hand == self.dealer_hand and not reveal) else \
        self.resources.card_images[card]

        # Animation of moving the card
        for step in range(35):
            current_pos = (
                start_pos[0] + (end_pos[0] - start_pos[0]) * step // 35,
                start_pos[1] + (end_pos[1] - start_pos[1]) * step // 35
            )
            self.renderer.draw_background()
            self.renderer.draw_game(self.player_balance, self.player_hand.value(),
                                    self.dealer_hand.value(), self.active, [], False, self.level,
                                    self.level_requirements[self.level])
            self.renderer.draw_cards(self.player_hand, self.dealer_hand, self.reveal_dealer_hand)
            self.screen.blit(card_image, current_pos)
            pygame.display.update()
            self.timer.tick(FPS)

        # Ensure the final position is correct
        hand.add_card(card)
        self.renderer.draw_background()
        self.renderer.draw_game(self.player_balance, self.player_hand.value(),
                                self.dealer_hand.value(), self.active, [], False, self.level,
                                self.level_requirements[self.level])
        self.renderer.draw_cards(self.player_hand, self.dealer_hand, self.reveal_dealer_hand)
        pygame.display.update()

    def dealer_turn(self):
        while (self.dealer_hand.value() <= 18 and self.dealer_hand.has_ace()) or self.dealer_hand.value() <= 17:
            self.animate_card_deal(self.dealer_hand, self.deck.deal_card(), reveal=False)

        # Reveal dealer's cards
        pygame.time.wait(1000)

        self.reveal_dealer_hand = True
        self.renderer.draw_background()
        self.renderer.draw_game(self.player_balance, self.player_hand.value(),
                                self.dealer_hand.value(), self.active, [], True, self.level,
                                self.level_requirements[self.level])
        self.renderer.draw_cards(self.player_hand, self.dealer_hand, self.reveal_dealer_hand)
        pygame.time.wait(1000)
        pygame.display.update()

    def handle_events(self, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.win:
                    self.win = False
                if event.key == pygame.K_y and not self.active:
                    self.deck = deck.Deck()
                    self.deal_initial_cards()
            if event.type == pygame.MOUSEBUTTONDOWN and not self.win:
                if not self.active:
                    if buttons[0].collidepoint(event.pos):  # Deal button
                        self.active = True
                        self.initial_deal = True
                        self.deck = deck.Deck()
                        self.reveal_dealer_hand = False
                        self.game_started = True
                        self.round_result_checked = False
                        if not self.level_up:  # Only deal cards if the player is not moving to the next level
                            self.deal_initial_cards()
                        self.level_up = False
                else:
                    if buttons[0].collidepoint(event.pos):  # Hit button
                        try:
                            self.animate_card_deal(self.player_hand, self.deck.deal_card())
                            if self.player_hand.value() > 21:
                                self.renderer.draw_game(self.player_balance, self.player_hand.value(),
                                                        self.dealer_hand.value(), self.active, [], False, self.level,
                                                        self.level_requirements[self.level])
                                self.renderer.draw_cards(self.player_hand, self.dealer_hand, self.reveal_dealer_hand)
                                pygame.display.update()
                                pygame.time.wait(500)
                                self.active = False
                                self.reveal_dealer_hand = True
                                self.renderer.draw_text("You Lose!", self.resources.font, white, WIDTH / 2, HEIGHT / 2)
                        except ValueError:
                            return 'deck_empty'

                    if buttons[1].collidepoint(event.pos):  # Stand button
                        self.dealer_turn()
                        self.active = False

    def check_round_result(self):
        if not self.level_up and not self.active and self.reveal_dealer_hand and not self.round_result_checked:
            player_value = self.player_hand.value()
            dealer_value = self.dealer_hand.value()

            if player_value > 21:
                round_result = "lose"
            elif (player_value > 21 and dealer_value > 21):
                round_result = "draw"
            elif player_value == dealer_value < 21:
                round_result = "draw"
            elif dealer_value > 21:
                round_result = "win"
            elif player_value > dealer_value:
                round_result = "win"
            elif player_value < dealer_value and player_value <= 21:
                round_result = "lose"
            else:
                round_result = "draw"

            if round_result == "lose":
                self.renderer.draw_text("You Lose!", self.resources.font, white, WIDTH / 2, HEIGHT / 2)
                self.player_balance -= 10
            elif round_result == "win":
                self.renderer.draw_text("You Win!", self.resources.font, white, WIDTH / 2, HEIGHT / 2)
                self.player_balance += 10
            elif round_result == "draw":
                self.renderer.draw_text("It's a Tie!", self.resources.font, white, WIDTH / 2, HEIGHT / 2)

            self.round_result_checked = True
            pygame.display.update()
            pygame.time.wait(2000)

            # Check if the player has won a level
            if self.player_balance >= self.level_requirements[self.level]:
                self.win = True
                if self.level == 3:
                    self.renderer.draw_win_screen(self.player_balance, is_game_won=True)
                else:

                    self.renderer.draw_win_screen(self.player_balance)
                self.player_balance = 100.0  # Reset the player's balance to 100 dollars after every level
            elif self.player_balance <= 0:
                self.renderer.draw_loss_screen()
            else:
                self.reveal_dealer_hand = False

            if self.player_balance >= self.level_requirements[self.level]:
                self.win = True
                self.renderer.draw_win_screen(self.player_balance)
                self.level_up = True  # Set the level up flag to True

    def game_loop(self):
        while True:
            buttons = []
            self.renderer.draw_game(self.player_balance, self.player_hand.value(),
                                    self.dealer_hand.value(), self.active, buttons, False, self.level,
                                    self.level_requirements[self.level])
            self.renderer.draw_cards(self.player_hand, self.dealer_hand, self.reveal_dealer_hand)
            action = self.handle_events(buttons)
            if action == 'menu':
                return
            if action == 'deck_empty':
                self.renderer.draw_deck_empty_screen()
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            self.deck = deck.Deck()
                            self.deal_initial_cards()
                            break

            if self.active:
                pass
            else:
                if not self.active and self.reveal_dealer_hand and not self.round_result_checked and not self.level_up:
                    self.check_round_result()

            if self.win:
                # Wait for the player to press a key before continuing to the next round
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.win = False
                            if self.level < 3:
                                self.level += 1
                                self.round_result_checked = False  # Reset the round result checked flag
                                self.player_balance = 100.0  # Reset the player's balance to 100 dollars
                                self.player_hand.clear()  # Reset the player's hand
                                self.dealer_hand.clear()  # Reset the dealer's hand
                                break  # Break the loop to continue the game
                            else:
                                # Display a different prompt after completing level 3
                                pygame.display.update()
                                pygame.time.wait(2000)
                                return  # Return to the main menu after level 3
                        elif event.key == pygame.K_ESCAPE:
                            return  # Return to the main menu when escape key is pressed

            # Redraw the background and the game elements after the 'Enter' key is pressed
            self.renderer.draw_background()
            self.renderer.draw_game(self.player_balance, self.player_hand.value(), self.dealer_hand.value(),
                                    self.active, [], False, self.level,
                                    self.level_requirements[self.level])
            self.renderer.draw_cards(self.player_hand, self.dealer_hand, self.reveal_dealer_hand)

            pygame.display.update()
            self.timer.tick(FPS)

    def reset_game(self):
        self.player_hand = hand.Hand()
        self.dealer_hand = hand.Hand()
        self.deck = deck.Deck()
        self.active = False
        self.initial_deal = False
        self.reveal_dealer_hand = False
        self.player_balance = 100.0
        self.win = False
        self.game_started = False
        self.round_result_checked = False
        self.level = 1
        self.level_up = False