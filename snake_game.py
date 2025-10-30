"""
Snake game implementation.
"""
import pygame
import random
import sys


class GameObject:
    """Base game object class."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen, cell_size):
        rect = (self.x * cell_size, self.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, self.color, rect)


class Apple(GameObject):
    """Apple food for snake."""
    def __init__(self, x, y):
        super().__init__(x, y, (255, 0, 0))

    def respawn(self, width, height, snake_body):
        while True:
            self.x = random.randint(0, width - 1)
            self.y = random.randint(0, height - 1)
            if (self.x, self.y) not in snake_body:
                break


class Snake:
    """Snake player class."""
    def __init__(self, width, height, cell_size):
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.direction = (1, 0)
        self.length = 1
        self.positions = [((width // 2), (height // 2))]
        self.color = (0, 255, 0)

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x) % self.width
        new_y = (head_y + dir_y) % self.height
        new_position = (new_x, new_y)

        if new_position in self.positions[1:]:
            self.reset()
            return False

        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [((self.width // 2), (self.height // 2))]
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def grow(self):
        self.length += 1

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self, screen):
        for position in self.positions:
            x_pos = position[0] * self.cell_size
            y_pos = position[1] * self.cell_size
            rect = (x_pos, y_pos, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, self.color, rect)


def main():
    """Main game function."""
    pygame.init()
    screen_width = 800
    screen_height = 600
    grid_size = 20
    grid_width = screen_width // grid_size
    grid_height = screen_height // grid_size

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake(grid_width, grid_height, grid_size)
    apple = Apple(random.randint(0, grid_width - 1),
                  random.randint(0, grid_height - 1))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        if not snake.move():
            apple.respawn(grid_width, grid_height, snake.positions)

        if snake.get_head_position() == (apple.x, apple.y):
            snake.grow()
            apple.respawn(grid_width, grid_height, snake.positions)

        screen.fill((0, 0, 0))
        snake.draw(screen)
        apple.draw(screen, grid_size)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
