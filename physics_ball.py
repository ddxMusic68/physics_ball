import pygame
import math

class Ball:
    ball_list = []
    id = 0
    def __init__(self, x_pos: float = 0, y_pos: float = 0, radius: float = 20, color = 'red', mass:float = 100, retention:float = 0.8, y_speed: float = 0, x_speed: float = 0, friction: float = 0.99):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.friction = friction
        self.selected = False
        self.prev_pos = (0, 0)
        self.id = Ball.id
        Ball.id += 1
        Ball.ball_list.append(self)

    def update_gravity(self, gravity: float = 0.5, bounce_stop: float = 0.1):
        self.y_speed += gravity
    
    def bounce_x(self, bounce_stop: float = 4):
        self.x_speed *= -self.retention
        if abs(self.x_speed) < bounce_stop:
            self.x_speed = 0

    def bounce_y(self, bounce_stop: float = 4):
        self.y_speed *= -self.retention
        if abs(self.y_speed) < bounce_stop:
            self.y_speed = 0

    def friction_x(self, friction_round: float = 0.1):
        self.x_speed *= self.friction
        if abs(self.x_speed) < friction_round:
            self.x_speed = 0
        
    def update_position(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed

    def collide(self, pos: tuple):
        x_length = abs(self.x_pos - pos[0])
        y_length = abs(self.y_pos - pos[1])
        total_length = math.sqrt(y_length**2 + x_length**2)
        if total_length < self.radius:
            return True
        return False

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x_pos, self.y_pos), self.radius)

    # mouse
    def collide_mouse(self, mouse_pos, left_click):
        x = mouse_pos[0]
        y = mouse_pos[1]
        speedx = x - self.prev_pos[0]
        speedy = y - self.prev_pos[1]
        self.prev_pos = mouse_pos
        if not self.selected:
            if left_click and self.collide(mouse_pos):
                self.selected = True
        else:
            self.x_pos = x
            self.x_speed = speedx/1.3
            self.y_pos = y
            self.y_speed = speedy/1.3
            if not left_click:
                self.selected = False


# mainloop
def test():
    pygame.init()

    WIDTH = 1000
    HEIGHT = 600
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    
    FPS = 60
    timer = pygame.time.Clock()

    ball0 = Ball(radius=50)
    ball1 = Ball(color='blue')
    ball_list = Ball.ball_list

    def ball_bounce(ball):
    # print(ball.x_pos)
        if ball.x_pos < (ball.radius): # right wall bounce
            ball.x_pos = ball.radius
            ball.bounce_x()
        elif ball.x_pos > (WIDTH - ball.radius): # left wall bounce
            ball.x_pos = WIDTH - ball.radius
            ball.bounce_x()

        if ball.y_pos > HEIGHT-ball.radius: # floor bounce
            ball.y_pos = HEIGHT-ball.radius
            ball.bounce_y()
        if ball.y_pos < ball.radius: # ceiling bounce
            ball.y_pos = ball.radius
            ball.bounce_y()

        if ball.y_speed == 0 and ball.x_speed != 0: # slows balls down if rubbing against the floor
            ball.friction_x()

    running = True
    while running:
        timer.tick(FPS)
        window.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]

        # drawing
        for ball in ball_list:
            ball.update_gravity(0.5)
            ball_bounce(ball)
            ball.update_position()
            ball.collide_mouse(mouse_pos, left_click)
            ball.draw(window)
        pygame.display.flip() # updates entire display to show changes
    pygame.quit()


if __name__ == "__main__":
    test()