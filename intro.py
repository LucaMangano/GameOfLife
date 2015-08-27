import pygame
from buttons import Button

class Intro():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((400, 350), 0, 32)
        self.font = pygame.font.SysFont('Arial', 30)

        self.choices = ( Button('Small', self.screen, (50, 50), 300, 50, (170, 60), self.font),
                         Button('Medium', self.screen, (50, 150), 300, 50, (155, 160), self.font),
                         Button('Big', self.screen, (50, 250), 300, 50, (185, 260), self.font) )
        
        self.main()

    def main(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for choice in self.choices:
                        if choice.highlight and choice == self.choices[0]:
                            self.name = 0
                            self.running = False
                        elif choice.highlight and choice == self.choices[1]:
                            self.name = 1
                            self.running = False
                        elif choice.highlight and choice == self.choices[2]:
                            self.name = 2
                            self.running = False

            mouse_pos = pygame.mouse.get_pos()

            self.background()
            self.blit_title()
            
            for choice in self.choices:
                choice.blit_rect()
                choice.check_mouse(mouse_pos)
                choice.blit_name()

            pygame.display.update()
        pygame.display.quit()

    def background(self):
        self.screen.fill((100, 100, 100))

    def blit_title(self):
        text = self.font.render('How big do you want the grid?', True, (0, 0, 0))
        self.screen.blit(text, (35, 5))

    def __repr__(self):
        return '%d' % (self.name)
