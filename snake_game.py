import pygame
import random
import sys
import time


class GameObject:
    """Базовый класс для всех игровых объектов."""
    
    def __init__(self, x, y, color):
        """
        Инициализация игрового объекта.
        
        Args:
            x (int): Координата X объекта
            y (int): Координата Y объекта
            color (tuple): Цвет объекта в формате RGB
        """
        self.x = x
        self.y = y
        self.color = color
    
    def draw(self, screen, cell_size):
        """
        Отрисовка объекта на экране.
        
        Args:
            screen: Поверхность для отрисовки
            cell_size (int): Размер ячейки в пикселях
        """
        pygame.draw.rect(screen, self.color, 
                        (self.x * cell_size, self.y * cell_size, 
                         cell_size, cell_size))


class Apple(GameObject):
    """Класс яблока - еды для змейки."""
    
    def __init__(self, x, y):
        """
        Инициализация яблока.
        
        Args:
            x (int): Координата X яблока
            y (int): Координата Y яблока
        """
        super().__init__(x, y, (255, 0, 0)) 
    
    def respawn(self, width, height, snake_body):
        """
        Перемещение яблока в случайную позицию на поле.
        
        Args:
            width (int): Ширина игрового поля в ячейках
            height (int): Высота игрового поля в ячейках
            snake_body (list): Тело змейки для проверки коллизий
        """
        while True:
            self.x = random.randint(0, width - 1)
            self.y = random.randint(0, height - 1)
            
            if (self.x, self.y) not in snake_body:
                break


class Snake:
    """Класс змейки."""
    
    def __init__(self, width, height, cell_size):
        """
        Инициализация змейки.
        
        Args:
            width (int): Ширина игрового поля
            height (int): Высота игрового поля
            cell_size (int): Размер ячейки
        """
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.direction = (1, 0) 
        self.length = 1
        self.positions = [((width // 2), (height // 2))] 
        self.last = None
        self.color = (0, 255, 0)
    
    def get_head_position(self):
        """Получить позицию головы змейки."""
        return self.positions[0]
    
    def move(self):
        """Перемещение змейки."""
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
            self.last = self.positions.pop()
        
        return True
    
    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [((self.width // 2), (self.height // 2))]
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.last = None
    
    def grow(self):
        """Увеличение длины змейки."""
        self.length += 1
    
    def change_direction(self, direction):
        """Изменение направления движения змейки."""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def draw(self, screen):
        """Отрисовка змейки на экране."""
        for position in self.positions:
            pygame.draw.rect(screen, self.color, 
                            (position[0] * self.cell_size, position[1] * self.cell_size, 
                             self.cell_size, self.cell_size))


def main():
    """Основная функция игры."""
    pygame.init()
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    GRID_SIZE = 20
    GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
    GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
    FPS = 10
    
    BACKGROUND_COLOR = (0, 0, 0)
    SNAKE_COLOR = (0, 255, 0)
    APPLE_COLOR = (255, 0, 0)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()
    
    snake = Snake(GRID_WIDTH, GRID_HEIGHT, GRID_SIZE)
    apple = Apple(random.randint(0, GRID_WIDTH - 1), 
                  random.randint(0, GRID_HEIGHT - 1))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Обработка управления змейкой
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
        
        if not snake.move():
            apple.respawn(GRID_WIDTH, GRID_HEIGHT, snake.positions)
        
        if snake.get_head_position() == (apple.x, apple.y):
            snake.grow()
            apple.respawn(GRID_WIDTH, GRID_HEIGHT, snake.positions)
        
        screen.fill(BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen, GRID_SIZE)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
