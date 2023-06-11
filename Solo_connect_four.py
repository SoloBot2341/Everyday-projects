from connect_four_pieces import PIECES  
import pygame
import sys
import os

pygame.init()
RESET_EVENT = pygame.USEREVENT + 1

class CONNECTFOUR():
    def __init__(self):
        self.game_on = True
        self.screen_width, self.screen_height = 700,700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.circle_diameter = self.screen_width // 7
        self.circle_radius = self.circle_diameter // 2
        self.grid = [[0 for _ in range(7)] for _ in range(6)]  # A 7*6 grid filled with zeros
        self.pieces = PIECES(self.grid, self.screen_width, self.screen_height, self.screen)
        self.winner = "No_winner"
        self.frame_speed = 0
        self.images = []
        self.current_image = None
        self.winner_animation_folder = "winner_screen_4"

        pygame.time.set_timer(RESET_EVENT, 4000)

    def load_images(self):
        for file_name in os.listdir(self.winner_animation_folder):
            if file_name.endswith('.png') or file_name.endswith('.jpg'):
                image = pygame.image.load(os.path.join(self.winner_animation_folder, file_name))
                self.images.append(image)


    # Draw the board
    def draw_grid(self):
        for c in range(7):  # Iterate through columns
            for r in range(6):  # Iterate through rows
                x = c * self.circle_diameter + self.circle_radius
                y = self.screen_height - (r * self.circle_diameter + self.circle_radius)
                if self.pieces.grid[r][c] == 0:  # Empty cell
                    pygame.draw.circle(self.screen, (0, 0, 255), (x, y), self.circle_radius)
                elif self.pieces.grid[r][c] == 1:  # Red piece
                    pygame.draw.circle(self.screen, self.pieces.red, (x, y), self.circle_radius)
                elif self.pieces.grid[r][c] == 2:  # Yellow piece
                    pygame.draw.circle(self.screen, self.pieces.yellow, (x, y), self.circle_radius)

    def check_winner(self):
        # Check horizontal locations for win
        for c in range(7-3):
            for r in range(6):
                if self.grid[r][c] == self.grid[r][c+1] == self.grid[r][c+2] == self.grid[r][c+3] != 0:
                    self.winner = "We have a winner"
                    return self.grid[r][c]

        # Check vertical locations for win
        for c in range(7):
            for r in range(6-3):
                if self.grid[r][c] == self.grid[r+1][c] == self.grid[r+2][c] == self.grid[r+3][c] != 0:
                    self.winner = "We have a winner"
                    return self.grid[r][c]

        # Check positively sloped diagonals
        for c in range(7-3):
            for r in range(6-3):
                if self.grid[r][c] == self.grid[r+1][c+1] == self.grid[r+2][c+2] == self.grid[r+3][c+3] != 0:
                    self.winner = "We have a winner"
                    return self.grid[r][c]

        # Check negatively sloped diagonals
        for c in range(7-3):
            for r in range(3, 6):
                if self.grid[r][c] == self.grid[r-1][c+1] == self.grid[r-2][c+2] == self.grid[r-3][c+3] > 0:
                    self.winner = "We have a winner"
                    return self.grid[r][c]

        return 0  # No winner


    #This method resets the game state
    def reset_game(self):
        if self.winner == "We have a winner":
            pygame.event.post(pygame.event.Event(RESET_EVENT))
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)
            self.screen.fill((255,255,255))
            self.pieces.turn = "player_red"
            self.grid = [[0 for _ in range(7)] for _ in range(6)]  # A 7*6 grid filled with zeros
            self.pieces.grid = self.grid  # Add this line to reset the pieces


    def winner_animation(self):
        print(self.frame_speed)
        self.screen.fill((255,255,255))
        self.frame_speed += 0.1

        # If frame_speed reaches the length of images, reset it to 0
        if self.frame_speed >= len(self.images):
            self.frame_speed = 0

        # Set the current image
        self.current_image = self.images[int(self.frame_speed)]

        # Blit the image at the top left corner
        self.screen.blit(self.current_image, (0,0)) 
       
    def update(self):
        while self.game_on:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    self.game_on = False
                    pygame.quit()
                    sys.exit()
                elif events.type == RESET_EVENT:
                    self.reset_game()
                    self.winner = "No_winner"

            if self.winner == "No_winner":
                self.screen.fill((0, 0, 0))  # Clear the screen by filling it with black
                self.draw_grid()
                winner = self.check_winner()
                if winner:
                    self.winner = "We have a winner"
                    self.load_images()
            else:
                self.winner_animation()

            self.pieces.update()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = CONNECTFOUR()
    game.update()
