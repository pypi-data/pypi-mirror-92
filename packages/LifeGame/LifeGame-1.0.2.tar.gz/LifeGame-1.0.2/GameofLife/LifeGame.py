import sys
import time
import pygame
import random
from datetime import datetime


class LifeGame:

    def __init__(self, screen_width=840, screen_height=600, cell_size=10, alive_color=(0, 255, 255), dead_color=(0, 0, 0), max_fps=7):
        """
        Initialize grid, set default game state, initialize screen

        :param screen_width:
        :param screen_height:
        :param cell_size: Diameter of circles
        :param alive_color: RGB tuple e.g. (255,255,255)
        :param dead_color: RGB tuple e.g. (0,0,0)
        :param max_fps: framerate cap to limit game speed
        """

        pygame.init()
        self.screen_height = screen_height
        self.screen_width = screen_height
        self.cell_size = cell_size
        self.alive_color = alive_color
        self.dead_color = dead_color
        self.max_fps = max_fps

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clear_screen()
        pygame.display.flip()

        self.last_update_completed = 0
        self.desired_millisecs_between_updates = (1.0/self.max_fps)*1000.0

        self.active_grid = 0
        self.grids = []
        self.num_columns = int(self.screen_width/self.cell_size)
        self.num_rows = int(self.screen_height/self.cell_size)
        self.init_grids()

        self.paused = False
        self.game_over = False

    def init_grids(self):
        """
        Creates and stores the default active and inactive grid
        :return: None
        """
        def create_grid():
            """
            Creates an empty 2D grid
            """
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0]*self.num_columns
                rows.append(list_of_columns)
            return rows

        self.grids.append(create_grid())
        self.grids.append(create_grid())
        self.set_grid()
        print(self.grids[0])

    def set_grid(self, value=None, grid=0):
        """
        Set an entire grid at once. Set to a single value or random 0/1
        Examples:
            self.grid(0) --> all dead
            self.grid(1) --> all alive
            self.grid() --> random
            self.grid(None) --> random

        :param grid: Index of grid, for acitve/inactive (0 or 1)
        :param value: value to set the cell to (0 or 1)
        """
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                if value is None:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = value

                self.grids[grid][row][column] = cell_value

    def draw_grid(self):
        """
        Given the grid and cell states, draws the cells on the screen
        """
        self.clear_screen()
        r = int(self.cell_size/2)  # radius

        for column in range(self.num_columns):
            for row in range(self.num_rows):

                if self.grids[self.active_grid][row][column] == 1:
                    color = self.alive_color
                else:
                    color = self.dead_color

                pygame.draw.circle(self.screen,
                                   color,
                                   (int(column*self.cell_size+r), int(row*self.cell_size+r)),
                                   r,
                                   0)

        pygame.display.flip()

    def clear_screen(self):
        """
        Fills the whole screen with dead dead_color
        """
        self.screen.fill(self.dead_color)
        pygame.display.flip()

    def check_cell_neighbors(self, row, column):
        """
        Gets the number of alive neighbor cells, and determine the state of the cell for the next generation
        Determines whether it lives, survives, dies or is born

        :param row: row number of the cell to check
        :param row: column number of the cell to check
        :return: The state the cell should be in next gen (0 or 1)
        """

        def get_cell(r, c):
            """
            Gets the alive/dead (0/1) of an specific cell in the active grid

            :param c: column
            :param r: row
            """
            cell_value = 0
            try:
                cell_value = self.grids[self.active_grid][r][c]
            except:
                cell_value = 0
            return cell_value

        num_alive_neighbors = 0

        num_alive_neighbors += get_cell(row-1, column-1)
        num_alive_neighbors += get_cell(row-1, column)
        num_alive_neighbors += get_cell(row-1, column+1)
        num_alive_neighbors += get_cell(row, column-1)
        num_alive_neighbors += get_cell(row, column+1)
        num_alive_neighbors += get_cell(row+1, column-1)
        num_alive_neighbors += get_cell(row+1, column)
        num_alive_neighbors += get_cell(row+1, column+1)

        # Rules
        if self.grids[self.active_grid][row][column] == 1:  # alive
            if num_alive_neighbors > 3:  # overpopulation
                return 0
            if num_alive_neighbors < 2:  # Underpopulation
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:  # survives
                return 1
        elif self.grids[self.active_grid][row][column] == 0:  # dead
            if num_alive_neighbors == 3:  # comes to life
                return 1

        return self.grids[self.active_grid][row][column]

        # comes to life
        if self.grids[self.active_grid][row][column] == 0 and num_alive_neighbors == 3:
            return 1
        if num_alive_neighbors > 4:  # overpopulation
            return 0
        if num_alive_neighbors < 3:  # Underpopulation
            return 0
        if (num_alive_neighbors == 2 or num_alive_neighbors == 3) and self.grids[self.active_grid][row][column] == 1:
            return 1
        else:
            return 0

    def update_generation(self):
        """
        Inspects current generation and prepares de the next one
        """

        self.set_grid(0, self.inactive_grid())

        for row in range(self.num_rows):
            for column in range(self.num_columns):
                next_gen_state = self.check_cell_neighbors(row, column)
                self.grids[self.inactive_grid()][row][column] = next_gen_state
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        """
        gets the number of the inactive grids
        if inactive grid is 0 will return 1 and viceversa
        """
        return (self.active_grid+1) % 2

    def event_handler(self):
        """
        Handle the key presses
        s - pause 
        q - quit
        r - randomize
        """

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.unicode == 's':
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True

                elif event.unicode == 'r':
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid)  # randomize
                    self.set_grid(0, self.inactive_grid())  # set to 0
                    self.draw_grid()

                elif event.unicode == 'q':
                    self.game_over = True

            if event.type == pygame.QUIT:
                sys.exit()

    def cap_frame_rate(self):
        """
        makes the game wait if its going too fast
        """

        now = pygame.time.get_ticks()
        millisecs_since_last_update = now - self.last_update_completed
        time_to_sleep = self.desired_millisecs_between_updates - millisecs_since_last_update

        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_completed = now

    def run(self):
        """
        starts and loops the game
        """
        while True:
            if self.game_over:
                return

            self.event_handler()

            if self.paused:
                continue

            self.update_generation()
            self.draw_grid()
            self.cap_frame_rate()


if __name__ == '__main__':
    """
    Launches a game of Life
    """
    game = LifeGame()
    game.run()
