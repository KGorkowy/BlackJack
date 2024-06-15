import sys
import pygame
import blackjackGame

# FPS quantity
FPS = 60

# Inicjalizacja Pygame
pygame.init()


# Function to start the game
def main():
    game = blackjackGame.BlackjackGame()
    while True:
        start_button, exit_button = game.renderer.draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    game.reset_game()  # Reset the game state
                    game.game_loop()
                if exit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        game.timer.tick(FPS)


if __name__ == "__main__":
    main()
