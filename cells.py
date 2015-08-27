import pygame

class Cell():
    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos
        self.alive = False
        self.alive_next = None
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 14, 14)
        self.rect_neighbours = pygame.Rect(self.pos[0] - 3, self.pos[1] - 3, 20, 20)

    def blit(self):
        pygame.draw.rect(self.screen, (246, 172, 0), (self.pos[0], self.pos[1], 14, 14))

    def update_status(self):
        self.alive = self.alive_next

