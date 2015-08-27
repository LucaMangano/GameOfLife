import pygame
from buttons import Button
from cells import Cell

class Simulation():
    def __init__(self):
        pygame.init()
        self.d = 2
        
        self.screen = pygame.display.set_mode((250*self.d, 150*self.d + 50), 0, 32)
        self.cells = []

        self.check_gen = False
        self.gens = 0
        self.font = pygame.font.SysFont('Arial', 15)

        self.buttons = ( Button('Reset', self.screen, (14, 150*self.d + 10), int(150*self.d/3), 30, (20, 150*self.d + 10), pygame.font.SysFont('Arial', 15)),
                         Button('Start', self.screen, (18 + int(150*self.d/3), 150*self.d + 10), int(150*self.d/3), 30, (24 + int(150*self.d/3), 150*self.d + 10), pygame.font.SysFont('Arial', 15)),
                         Button('Gen', self.screen, (22 + int(150*self.d/3)*2, 150*self.d + 10), int(150*self.d/3), 30, (28 + int(150*self.d/3)*2, 150*self.d + 10), pygame.font.SysFont('Arial', 15)),
                         Button('Normal', self.screen, (26 + int(150*self.d/3)*3, 150*self.d + 10), int(150*self.d/3), 30, (32 + int(150*self.d/3)*3, 150*self.d + 10), pygame.font.SysFont('Arial', 15)) )

        self.clock = pygame.time.Clock()
        self.timer = 0
        self.time_lapse = 0.2

        self.main()

    def main(self):
        restart = False
        running = True
        while running:
            time = self.clock.tick(30)
            time_seconds = time/1000.
            self.timer += self.clock.get_rawtime()/1000.
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.background()

            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_mouse(pos)
            if pygame.mouse.get_pressed()[0]:
                for button in self.buttons:
                    if button == self.buttons[0]:
                        button.click(pos)
                        if button.clicked:
                            running = False
                            restart = True
                    if button == self.buttons[1]:
                        button.click(pos)
                        if button.clicked:
                            if not self.check_gen:
                                self.check_gen = True
                                button.name = 'Stop'
                                self.timer = 0
                                pygame.time.wait(250)
                            elif self.check_gen:
                                self.check_gen = False
                                button.name = 'Start'
                                pygame.time.wait(250)
                        button.clicked = False
                    if button == self.buttons[3]:
                        button.click(pos)
                        if button.clicked:
                            if self.time_lapse == 0.01:
                                self.time_lapse = 0.5
                                button.name = 'Slow'
                                pygame.time.wait(250)
                            elif self.time_lapse == 0.5:
                                self.time_lapse = 0.2
                                button.name = 'Normal'
                                pygame.time.wait(250)
                            elif self.time_lapse == 0.2:
                                self.time_lapse = 0.1
                                button.name = 'Fast'
                                pygame.time.wait(250)
                            elif self.time_lapse == 0.1:
                                self.time_lapse = 0.01
                                button.name = 'Crazy'
                                pygame.time.wait(250)
                        button.clicked = False
                
            if self.check_gen and self.timer >= self.time_lapse:
                self.timer = 0
                self.check_generation()
                for cell in self.cells:
                    cell.update_status()
                self.gens += 1

            else:
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    self.check_cells_pos(mouse_pos)

            for cell in self.cells:
                if cell.alive:
                    cell.blit()

            for button in self.buttons:
                button.blit_rect()
                button.blit_name()

            button = self.buttons[2]
            button.name = 'Gen '+str(self.gens)

            pygame.display.update()
            
        pygame.display.quit()
        if restart:
            Simulation(self.d)

    def blit_text(self, words, pos):
        text = self.font.render(words, True, (0, 0, 0))
        self.screen.blit(text, pos)

    def background(self):
        self.screen.fill((100, 100, 100))

        x = 14
        y = 14
        for n in range(0, int(((250*self.d)-14)/14)):
            for n in range(0, int(((150*self.d)-14)/14)):
                pygame.draw.rect(self.screen, (50, 50, 50), (x, y, 14, 14), 1)
                y += 14
            x += 14
            y = 14

        if len(self.cells) == 0:
            x = 14
            y = 14
            for n in range(0, int(((250*self.d)-14)/14)):
                for n in range(0, int(((150*self.d)-14)/14)):
                    self.cells.append(Cell(self.screen, (x, y)))
                    y += 14
                x += 14
                y = 14

    def check_cells_pos(self, mouse_pos):
        for cell in self.cells:
            if cell.rect.collidepoint(mouse_pos):
                if not cell.alive:
                    cell.alive = True
       
    def check_generation(self):
        cells_alive_list = []
        for cell in self.cells:
            if cell.alive:
                cells_alive_list.append(cell.rect_neighbours)

        for cell in self.cells:
            if cell.alive:
                self.check_underpopulation(cells_alive_list, cell)
                self.check_overcrowding(cells_alive_list, cell)
                self.check_next_gen(cells_alive_list, cell)
            elif not cell.alive:
                self.check_neighbours(cells_alive_list, cell)

    def check_underpopulation(self, cells_alive_list, cell):
        if len(cell.rect_neighbours.collidelistall(cells_alive_list)) <= 2:
            cell.alive_next = False
            
    def check_overcrowding(self, cells_alive_list, cell):
        if len(cell.rect_neighbours.collidelistall(cells_alive_list)) >= 5:
            cell.alive_next = False

    def check_next_gen(self, cells_alive_list, cell):
        if len(cell.rect_neighbours.collidelistall(cells_alive_list)) == 3 or \
           len(cell.rect_neighbours.collidelistall(cells_alive_list)) == 4:
            cell.alive_next = True

    def check_neighbours(self, cells_alive_list, cell):
        if len(cell.rect_neighbours.collidelistall(cells_alive_list)) == 3:
            cell.alive_next = True
