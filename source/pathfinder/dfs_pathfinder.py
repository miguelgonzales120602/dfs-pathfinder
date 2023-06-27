import pygame;
import math

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("DFS Pathfinder")

CLOSED_COLOR = (66, 70, 140)
OPEN_COLOR = (245, 167, 200)
BG_COLOR = (240, 241, 249)
BARRIER_COLOR = (3, 10, 140)
PATH_COLOR = (92, 116, 245)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
        def __init__(self, row, col, width, total_rows):
                self.row = row
                self.col = col
                self.x = row * width
                self.y = col * width
                self.color = BG_COLOR
                self.neighbors = []
                self.width = width
                self.total_rows = total_rows

        def get_pos(self):
                return self.row, self.col

        def is_closed(self):
                return self.color == CLOSED_COLOR

        def is_open(self):
                return self.color == OPEN_COLOR

        def is_barrier(self):
                return self.color == BARRIER_COLOR

        def is_start(self):
                return self.color == ORANGE

        def is_end(self):
                return self.color == TURQUOISE

        def reset(self):
                self.color = BG_COLOR

        def make_start(self):
                self.color = ORANGE

        def make_closed(self):
                self.color = CLOSED_COLOR

        def make_open(self):
                self.color = OPEN_COLOR

        def make_barrier(self):
                self.color = BARRIER_COLOR

        def make_end(self):
                self.color = TURQUOISE

        def make_path(self):
                self.color = PATH_COLOR

        def draw(self, win):
                pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

        def update_neighbors(self, grid):
                self.neighbors = []
                if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Moving down
                        self.neighbors.append(grid[self.row + 1][self.col])

                if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Moving up
                        self.neighbors.append(grid[self.row - 1][self.col])

                if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Moving right
                        self.neighbors.append(grid[self.row][self.col + 1])

                if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Moving left
                        self.neighbors.append(grid[self.row][self.col - 1])

        def __lt__(self, other):
                return False

def algorithm(draw, grid, start, end):
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()

        if current == end:
            for node in path:
                node.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        if current not in visited:
            visited.add(current)
            current.make_closed()
            draw()

            for neighbor in current.neighbors:
                if neighbor not in visited and not neighbor.is_barrier():
                    stack.append((neighbor, path + [neighbor]))
                    neighbor.make_open()

    # Backtracking
    for node in path:
        if node != start and node != end:
            node.make_closed()
            draw()

    # Reset start and end node colors
    start.make_start()
    end.make_end()
    draw()

    return False

def make_grid(rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
                grid.append([])
                for j in range(rows):
                        node = Node(i, j, gap, rows)
                        grid[i].append(node)

        return grid

def draw_grid(win, rows, width):
        gap = width // rows
        for i in range(rows):
                pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
                for j in range(rows):
                        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
        win.fill(BG_COLOR)

        for row in grid:
                for node in row:
                        node.draw(win)

        draw_grid(win, rows, width)
        pygame.display.update()

def get_clicked_pos(pos, rows, width):
        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col

def main(win, width):
        ROWS = 50

        grid = make_grid(ROWS, width)

        start = None
        end = None

        run = True
        started = False

        while run:
                draw(win, grid, ROWS, width)
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                run = False

                        if started:
                                continue

                        if pygame.mouse.get_pressed()[0]: # LEFT
                                pos = pygame.mouse.get_pos()
                                row, col = get_clicked_pos(pos, ROWS, width)
                                node = grid[row][col]
                                if not start and node != end:
                                        start = node
                                        start.make_start()

                                elif not end and node != start:
                                        end = node
                                        end.make_end()

                                elif node != end and node != start:
                                        node.make_barrier()
                        elif pygame.mouse.get_pressed()[2]: # RIGHT
                                pos = pygame.mouse.get_pos()
                                row, col = get_clicked_pos(pos, ROWS, width)
                                node = grid[row][col]
                                node.reset()

                                if node == start:
                                        start = None
                                elif node == end:
                                        end = None

                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE and not started:
                                        for row in grid:
                                                for node in row:
                                                        node.update_neighbors(grid)

                                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                                if event.key == pygame.K_c:
                                        start = None
                                        end = None
                                        grid = make_grid(ROWS, width)
        pygame.quit()

main(WIN, WIDTH)
