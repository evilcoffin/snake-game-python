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
    
    return game_loop(screen, clock, snake, apple, grid_size, grid_width, grid_height)


def game_loop(screen, clock, snake, apple, grid_size, grid_width, grid_height):
    """Main game loop."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_input(event, snake)
        
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


def handle_input(event, snake):
    """Handle keyboard input."""
    if event.key == pygame.K_UP:
        snake.change_direction((0, -1))
    elif event.key == pygame.K_DOWN:
        snake.change_direction((0, 1))
    elif event.key == pygame.K_LEFT:
        snake.change_direction((-1, 0))
    elif event.key == pygame.K_RIGHT:
        snake.change_direction((1, 0))


if __name__ == "__main__":
    main()
