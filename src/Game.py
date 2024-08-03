import random
import pygame


class Game:
   
    def __init__(self, width: int, height: int, grid_cell: int):
        self.width = width
        self.height = height
        self.grid_cell = grid_cell

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True

        # self.mouse = Mouse(self.width, self.height)
        self.grid = [[0 for _ in range(self.width // self.grid_cell)] for _ in range(self.height // self.grid_cell)]
        self.hue = 0
    
    def update(self):
        while self.running:
            self.tick()
            self.render()

            pygame.display.flip()
            self.clock.tick(60)
            
    def render(self):
        self.screen.fill(color=(0, 0, 0))
        self.draw_grid()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.mouse()
        self.move_sand()

    def draw_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                rect = pygame.Rect(x * self.grid_cell, y * self.grid_cell, self.grid_cell, self.grid_cell)

                # Fill the cell if it has a value greater than 0
                if self.grid[y][x] > 0:
                    color = pygame.Color(0)
                    color.hsla = (self.grid[y][x], 100, 50, 100)
                    pygame.draw.rect(self.screen, color, rect)
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def move_sand(self):
        new_grid = [[0 for _ in range(self.width // self.grid_cell)] for _ in range(self.height // self.grid_cell)]
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 0:
                    continue
                
                # Check if the cell is at the bottom
                if y + 1 >= len(self.grid):
                    new_grid[y][x] = self.grid[y][x]
                    continue

                below_right = x + 1 < len(self.grid[y]) and self.grid[y+1][x+1] == 0
                below_left = x - 1 >= 0 and self.grid[y+1][x-1] == 0

                # Check if the cell below is empty
                if self.grid[y+1][x] == 0:
                    new_grid[y+1][x] = self.grid[y][x]
                    new_grid[y][x] = 0
                elif below_right:
                    new_grid[y+1][x+1] = self.grid[y][x]
                    new_grid[y][x] = 0
                elif below_left:
                    new_grid[y+1][x-1] = self.grid[y][x]
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = self.grid[y][x]

        self.grid = new_grid

    def mouse(self):
        # Check if the left mouse button is pressed
        if pygame.mouse.get_pressed()[0] is True:
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0] // self.grid_cell
            y = mouse_pos[1] // self.grid_cell

            #  Check if the mouse is out of bounds
            if x < 0 or x >= len(self.grid[0]) or y < 0 or y >= len(self.grid):
                return
            
            # Check if the cell is already filled
            if self.grid[y][x] > 0:
                return
            
            # Check if you can generate sand at this time
            if random.random() > 0.5:
                return

            self.grid[y][x] = self.hue
            self.hue = self.hue + 1 if self.hue < 360 else 0