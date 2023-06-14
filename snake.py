import pygame
import random

# 游戏窗口的大小
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 蛇身和食物的大小
CELL_SIZE = 20

# 蛇的移动速度
SNAKE_SPEED = 10

# 定义颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
white = (255, 255, 255)

# 初始化 Pygame
pygame.init()

# 创建游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')

clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.color = white

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction

        new = ((cur[0] + (x * CELL_SIZE)) % WINDOW_WIDTH, (cur[1] + (y * CELL_SIZE)) % WINDOW_HEIGHT)

        if len(self.positions) > 2 and new in self.positions[2:]:
            return False  # 返回 False 表示游戏结束

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], CELL_SIZE, CELL_SIZE))


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, WINDOW_WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                         random.randint(0, WINDOW_HEIGHT // CELL_SIZE - 1) * CELL_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))


snake = Snake()
food = Food()

running = True
game_over = False  # 标志游戏是否结束
in_menu = True  # 标志是否在菜单界面
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if in_menu:
                in_menu = False
            elif game_over:
                if event.key == pygame.K_SPACE:
                    snake.reset()
                    game_over = False
                    score = 0
        elif event.type == pygame.KEYUP:
            if not game_over and not in_menu:
                if event.key == pygame.K_UP or event.key ==pygame.K_w and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN or event.key ==pygame.K_s and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT or event.key ==pygame.K_a and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT or event.key ==pygame.K_d and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

    if not in_menu:
        if not game_over:
            game_over = not snake.update()

            if snake.get_head_position() == food.position:
                snake.length += 1
                food.randomize_position()
                score += 1

        window.fill(BLACK)
        snake.draw(window)
        food.draw(window)

        # 显示分数
        font = pygame.font.Font(None, 24)
        score_text = font.render("Score: " + str(score), True, GREEN)
        score_rect = score_text.get_rect()
        score_rect.topright = (WINDOW_WIDTH - 10, 10)
        window.blit(score_text, score_rect)

        if game_over:
            # 绘制游戏结束的提示信息
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over! Press Space to Restart", True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            window.blit(text, text_rect)
    else:
        # 绘制游戏菜单
        font = pygame.font.Font(None, 36)
        text = font.render("Press any key to start", True, GREEN)
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        window.blit(text, text_rect)

    pygame.display.update()
    clock.tick(SNAKE_SPEED)

pygame.quit()
