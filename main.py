#  -*- coding: utf-8 -*-
import pygame
import sys
from pygame.locals import *
from Button import init_buttons
from Bio import Bio
import time

K = 1.6
RIGHT_PANEL = 460
FPS = 36
MODES = [u'М4', u'М5', u'М7', u'М8', u'М9']
TURN_ON_BUTTONS = [u'Р', u'КР', u'ММ', u'2', u'Э', u'ЭА', u'ЭТ', u'КТ', u'45', u'200'] + \
                  [u'Є', u'ЭА/ЭС', u'О/ОС', u'П/ГЗ', u'МДА', u'МО', u'ТРМ', u'ЗН', u'ЛИН', u'ЗУМ']


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
        self.is_on = False

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
            if event.key == pygame.K_z:
                self.bio.signs = []
            if event.key == pygame.K_m:
                self.is_on = True
                for b in TURN_ON_BUTTONS:
                    self.buttons[b].pressed = True
            if event.key == pygame.K_l:
                self.init_bio()

    def on_loop(self):
        if self.is_on:
            self.bio.tick()

        self.analyze_stack()

    def on_render(self):
        start = time.time()
        for val in self.buttons.itervalues():
            if val.updated:
                val.draw(self._display_surf)
                val.updated = False

        self.bio.draw(self._display_surf, self)

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            start = time.time()
            self.on_loop()
            start = time.time()
            self.on_render()
            start = time.time()
            self.clock.tick(FPS)
            ## print time.time() - start, "CLOCK"

        self.on_cleanup()

    def analyze_stack(self):
        if not self.stack:
            return
        if self.stack[-1] in MODES:
            # ЕСЛИ НЕ ПРАВДА ЧТО КНОПКА НАЖАТА (БЫЛА НЕ НАЖАТА)
            if not self.buttons[self.stack[-1]].pressed:
                self.mode = 0
            else:
                for m in MODES:
                    if m != self.stack[-1]:
                        self.buttons[m].pressed = False

                self.mode = int(self.stack[-1][-1])
            self.stack = []
        elif self.stack[-1] == u'ВВОД':
            if self.mode == 7:
                if self.stack[-2:] == [u"1В", u"ВВОД"]:
                    self.bio.tasks_stack.append(["first_enter", self.bio.KT])
                elif self.stack[-3:] == [u"ЗП", u"СК1", u"ВВОД"]:
                    self.bio.tasks_stack.append(["special_correction1", self.bio.KT])
                elif self.stack[-3:] == [u"ЗП", u"СК2", u"ВВОД"]:
                    self.bio.tasks_stack.append(["special_correction2", self.bio.KT])
                elif len(self.stack) == 1:
                    self.bio.tasks_stack.append(["simple_correction", self.bio.KT])

            self.stack = []
        elif self.stack[-1] == u'СМ':
            if all([self.buttons[x].pressed for x in TURN_ON_BUTTONS]):
                self.is_on = True
            self.stack = []




if __name__ == "__main__":
    if 'LOWFPS' in sys.argv:
        FPS = 24
    theApp = App()
    theApp.on_execute()