import pygame

class Button():
    def __init__(self, name, screen, rect_pos, w, h, text_pos, font):
        self.screen = screen
        self.name = name
        self.rect_pos = rect_pos
        self.text_pos = text_pos
        self.highlight = False
        self.w = w
        self.h = h
        self.font = font
        self.clicked = False

    def check_mouse(self, mouse_pos):
        x, y = mouse_pos
        if x >= self.rect_pos[0] and x <= self.rect_pos[0] + self.w:
            if y >= self.rect_pos[1] and y <= self.rect_pos[1] + self.h:
                self.highlight_bg()
                self.highlight = True
        else:
            self.highlight = False
                
        
    def blit_rect(self):
        pygame.draw.rect(self.screen, (150, 150, 150), (self.rect_pos[0], self.rect_pos[1], self.w, self.h), 2)

    def blit_name(self):
        text = self.font.render(self.name, True, (0, 0, 0))
        self.screen.blit(text, self.text_pos)

    def highlight_bg(self):
        pygame.draw.rect(self.screen, (200, 200, 200), (self.rect_pos[0] + 2, self.rect_pos[1] + 2, self.w - 3, self.h - 3))

    def click(self, mouse_pos):
        x, y = mouse_pos
        if x >= self.rect_pos[0] and x <= self.rect_pos[0] + self.w:
            if y >= self.rect_pos[1] and y <= self.rect_pos[1] + self.h:
                self.clicked = True     

