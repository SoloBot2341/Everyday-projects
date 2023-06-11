import pygame

class PIECES():
    def __init__(self, grid, width, height, screen):
        self.screen = screen
        self.grid = grid
        self.width, self.height = width, height
        self.circle_diameter = self.width // 7
        self.circle_radius = self.circle_diameter // 2
        self.turn = "player_red"
        self.red, self.yellow = (255, 0, 0), (255, 255, 0)

    def find_position(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                column = x // self.circle_diameter
                for row in range(6):  # start from the bottom of the column
                    if self.grid[row][column] == 0:  # check if the spot is empty
                        return row, column  # return the first empty spot from the bottom


            
    def draw_pieces(self, row, column):
        x = (column * self.circle_diameter) + self.circle_radius
        y = self.height - ((row+1) * self.circle_diameter - self.circle_radius)  # Adjust the y coordinate, too
        if self.turn == "player_red":
            pygame.draw.circle(self.screen, self.red, (x, y), self.circle_radius)
            self.grid[row][column] = 1  # Represent a red piece as 1
            self.turn = "player_yellow"
        else:
            pygame.draw.circle(self.screen, self.yellow, (x, y), self.circle_radius)
            self.grid[row][column] = 2  # Represent a yellow piece as 2
            self.turn = "player_red"


    def update(self):
        pos = self.find_position()
        if pos is not None:
            self.draw_pieces(*pos)
