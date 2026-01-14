import pygame
from entity import Entity
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(Entity):
    def __init__(self, x, y, speed=5):
        super().__init__(x, y)
        self.speed = speed
        self.width = 50
        self.height = 30
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
   
    def controle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
    
    def clamp(self):
        self.y = SCREEN_HEIGHT - self.height - 10
        if self.x < 0:
            self.x = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
    
    def update(self):
        self.controles()
        self.clamp()
        self.rect.topleft = (self.x, self.y)
   
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
