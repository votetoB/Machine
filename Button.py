# -*- coding: utf-8 -*-
import pygame
K = 1.6
RIGHT_PANEL = 460
FPS = 120

import time


def init_buttons(self):
    self.buttons = dict()
    prm = [
        [u'Р', u'К', u'АК', u'В', u''],
        [u'КР', u'ДА', u'ДУ', u'ДАУ', u'ВР'],
        [u'22.5', u'45', u'90', u'180', u'360'],
        [u'100', u'200', u'400', u'800', u''],
        [u'ММ', u'МР', (u'СМ', False), u'БС', u'С'],
    ]
    pu = [
        [u'1', u'2', u'3', u'4', u'ЗВ'],
        [u'Э', u'ЭА', u'ЭС', u'П', u'ГЗ'],
        [u'О', u'ОК', u'КС', u'', (u'ЗО', False)],
        [u'ПР', u'ВЛ', u'ВВ', u'ЭТ', u'КТ'],
        [u'СО', u'ОЗ', u'ОС', u'ИМ', (u'КЗ', False)]
    ]

    bio_buttons = [u'Є', u'ЭА/ЭС', u'О/ОС', u'П/ГЗ', u'МДА', u'МО', u'ТРМ', u'ЗН', u'ЛИН', u'ЗУМ']

    buttons_texts41 = [repr(i) for i in range(1, 13)]
    buttons_texts42 = [u'', u'', u'', u'М4', u'М5', u'', u'М7', u'М8', u'М9', u'', (u'Х', False), (u'ЮК', False)]
    buttons_texts43 = [u'ВВОД', u'1В', u'ЗП', u'СК1', u'СК2', u'ИС', u'№ВО', u'ПЗ', u'КО', u'ЛУПА', u'Ф', u'ИСТ', u'СБ']

    x, y = 460 * 1.6, 45 * 1.6
    width, height = 24 * 1.6, 24 * 1.6
    space = 5

    for row in prm:
        x = 460 * 1.6
        for el in row:
            if not isinstance(el, tuple):
                self.buttons[el] = Button(el, True, (100, 100, 100), (x, y), (width, height))
            else:
                self.buttons[el[0]] = Button(el[0], False, (100, 100, 100), (x, y), (width, height))
            x += width + space

        y += height + space

    y += space

    for row in pu:
        x = 460 * 1.6
        for el in row:
            if not isinstance(el, tuple):
                self.buttons[el] = Button(el, True, (100, 100, 100), (x, y), (width, height))
            else:
                self.buttons[el[0]] = Button(el[0], False, (100, 100, 100), (x, y), (width, height))

            x += width + space

        y += height + space

    x = 50
    y = 550
    for el in bio_buttons:
        self.buttons[el] = Button(el, True, (100, 100, 100), (x, y), (width, height))
        x += width + space

    y += height + space
    x = 50

    for el in buttons_texts41:
        self.buttons[el + 'N'] = Button(el, False, (100, 100, 100), (x, y), (width, height))
        x += width + space

    y += height + space

    x = 50
    for el in buttons_texts42:
        if not isinstance(el, tuple):
            self.buttons[el] = Button(el, True, (100, 100, 100), (x, y), (width, height))
        else:
            self.buttons[el[0]] = Button(el[0], False, (100, 100, 100), (x, y), (width, height))
        x += width + space

    y += height + space

    x = 50
    for el in buttons_texts43:
        self.buttons[el] = Button(el, False, (100, 100, 100), (x, y), (width, height))

        x += width + space


class Button:
    def __init__(self, text="Text", checkable=True, color=(0, 0, 0), position=(0, 0), size=(20, 20),
                 pressed=False, width=1):
        self.text = text
        self.checkable = checkable
        self.color = color
        self.position = position
        self.size = size
        self.pressed = pressed
        self.width = width
        self.updated = True

    def __bool__(self):
        return self.pressed

    def on_press(self, app, s="down"):
        if s == "down":
            self.pressed = 1 - self.pressed
            self.updated = True
        elif s == "up":
            app.stack.append(self.text)
            if not self.checkable:
                self.pressed = False
            self.updated = True

    def write_text(self, surface, text_color):
        if len(self.text) == 0:
            return surface
        font_size = int(self.size[0]//3)
        myFont = pygame.font.SysFont("Arial", font_size)
        myText = myFont.render(self.text, 1, text_color)
        surface.blit(myText, ((self.position[0]+self.size[0]/2) - myText.get_width()/2, (self.position[1]+self.size[
            1]/2) - myText.get_height()/2))
        return surface

    def draw(self, surface):
        for i in range(1, 10):
            s = pygame.Surface((self.size[0] + (i*2), self.size[1]+(i*2)))
            s.fill((255, 255, 255))
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, self.color, (self.position[0]-i, self.position[1]-i, self.size[0]+i, self.size[1]+i),
                             self.width)
            surface.blit(s, (self.position[0]-i,self.position[1]-i))
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.size[0], self.size[1]), 0)
        pygame.draw.rect(surface, (190, 190, 190), (self.position[0], self.position[1], self.size[0],
        self.size[1]), 1)
        if self.pressed:
            self.write_text(surface, (255, 255, 0))
        else:
            self.write_text(surface, (0, 0, 0))

        return surface

    def collides(self, point):
        return (self.position[0] <= point[0] <= (self.position[0] + self.size[0])) and \
            (self.position[1] <= point[1] <= (self.position[1] + self.size[1]))
