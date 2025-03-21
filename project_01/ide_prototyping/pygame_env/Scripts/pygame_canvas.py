import pygame
import sys

class PygameCanvas:
    def __init__(self):
        pygame.init()
        self.width, self.height = 320, 240
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Pygame Canvas')

        self.colors = [(0, 0, 0), (255, 0, 0), (255, 165, 0), (255, 204, 0),
                       (0, 255, 0), (0, 0, 255), (75, 0, 130), (255, 192, 203)]
        self.color_index = 0
        self.current_color = self.colors[self.color_index]
        
        self.color_button_rect = pygame.Rect(10, 10, 80, 30)
        self.clear_button_rect = pygame.Rect(100, 10, 80, 30)

        self.drawing = False
        self.running = True

    def draw_button(self, text, rect, color):
        pygame.draw.rect(self.screen, color, rect)
        font = pygame.font.Font(None, 24)
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def refresh_screen(self):
        self.draw_button("Color", self.color_button_rect, self.current_color)
        self.draw_button("Clear", self.clear_button_rect, (0, 0, 0))
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill((255, 255, 255))
        self.refresh_screen()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.color_button_rect.collidepoint(event.pos):
                    self.color_index = (self.color_index + 1) % len(self.colors)
                    self.current_color = self.colors[self.color_index]
                    self.refresh_screen()
                elif self.clear_button_rect.collidepoint(event.pos):
                    self.clear_screen()
                else:
                    self.drawing = True
                    pygame.draw.circle(self.screen, self.current_color, event.pos, 3)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
            elif event.type == pygame.MOUSEMOTION and self.drawing:
                pygame.draw.circle(self.screen, self.current_color, event.pos, 3)

    def run(self):
        self.clear_screen()
        self.refresh_screen()
        while self.running:
            self.handle_events()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = PygameCanvas()
    app.run()
