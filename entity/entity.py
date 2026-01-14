import pygame
import settings

class Entity:
    def __init__(self, x, y, color=settings.GREEN, speed=5):
        self.size = min(settings.WINDOW_WIDTH,settings.WINDOW_HEIGHT)// 15
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def vitesse(self, speed):
        self.speed = speed
    
    def couleur(self, color):
        self.color = color
 
    def move_horizontal(self, direction):
        self.rect.x += direction * self.speed
        self.rect.x = max(0, min(self.rect.x, settings.WINDOW_WIDTH - self.size))
    
    def move_vertical(self, direction):
        self.rect.y += direction * self.speed
        self.rect.y = max(0, min(self.rect.y, settings.WINDOW_HEIGHT - self.size))
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)