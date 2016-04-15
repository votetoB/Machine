#  -*- coding: utf-8 -*-
import pygame
import sys
from pygame.locals import *
from Button import Button, init_buttons
from Bio import Bio

K = 1.6
RIGHT_PANEL = 460
FPS = 1500
MODES = [u'М4', u'М5', u'М7', u'М8', u'М9']

class App:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1024, 768
        self.mode = None
        init_buttons(self)
        self.init_bio()
        self.stack = []

    def init_bio(self):
        self.bio = Bio()

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("KZA 86G6")
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill((250, 250, 250))

        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for key, val in self.buttons.iteritems():
                if val.collides(pos):
                    val.on_press(self, "down")

            if self.bio.collides(pos):
                self.bio.on_click(pos)

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for key, val in self.buttons.iteritems():
                if val.collides(pos):
                    val.on_press(self, "up")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                self.bio.swap_traces_visibility()
            if event.key == pygame.K_f:
                self.bio.swap_temp_places_visibility()



    def on_loop(self):
        self.clock.tick(FPS)
        self.bio.tick()
        self.analyze_stack()

    def on_render(self):
        for key, val in self.buttons.items():
            val.draw(self._display_surf)

        self.bio.draw(self._display_surf)

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def analyze_stack(self):
        if not self.stack:
            return
        if self.stack[-1] in MODES:
            self.mode = int(self.stack[-1][-1])
            self.stack.pop()
        if u'ВВОД' in self.stack:
            if self.stack[-1] == u'ВВОД':
                self.stack = []
            else:
                self.stack = []


if __name__ == "__main__":
    if 'LOWFPS' in sys.argv:
        FPS = 24
    theApp = App()
    theApp.on_execute()