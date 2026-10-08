import pygame
import sys
from pygame.locals import *

# ensure parent folder is in the search path
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# import config files
from config.mst import *
import engine.render as render

pygame.init()
pygame.display.set_caption('Renderer')

class Main:
    def __init__(self):
        self.win = pygame.display.set_mode(WINDOWSIZE)
        self.dis = pygame.Surface(DISPLAYSIZE)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.fps = 0
        self.fps_tick = 0

        #self.cube = render.Cube(
        #    self, (0, 0, 20), (20, 20, 20), 0
        #)
        self.sphere = render.Sphere(
            self, (0, 0, 45), 40, 0
        )

    def run(self):
        while 1:
            self.fps += 1
            fps = self.clock.get_fps()
            if self.fps >= fps:
                self.fps_tick += 1
                self.fps = 0
            if self.fps_tick >= 1:
                self.fps_tick = 0
                print(int(fps))
            self.dt = self.clock.tick(10_000) / 1000

            self.sphere.svertex_proc()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.dis.fill((0, 0, 0))

            self.sphere.srender()

            self.win.blit(
                pygame.transform.scale(self.dis, WINDOWSIZE), (0, 0)
            )
            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
