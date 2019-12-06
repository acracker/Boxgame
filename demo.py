#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-12-6 下午4:24
# @Author  : pang
# @File    : demo.py
# @Software: PyCharm


import pygame as pg

# Vector可以看成(x,y)的封装
vec = pg.math.Vector2


Game_Map_Source = []
Game_Step = 0
Player_Pos=[0,0]
Game_Level = 1
Game_Map = []
Map_Wide = 0
Map_Deepth = 0
Game_Path = []
Dir = ((-1,0),(1,0),(0,-1),(0,1))
Game_Map_Size = 64
MAX_STEP = 12
BackgroundSize = Game_Map_Size * MAX_STEP

#Global Var Done

# Game_font = pg.font.SysFont("arial",32)
#
# Image_Help          =   pg.image.load("source/help.png").convert()
# Image_Welcome       =   pg.image.load("source/welcome.png").convert()
# Image_Box_Inplace   =   pg.image.load("source/Box_Inplace.jpg").convert()
# Image_Box_Outplace  =   pg.image.load("source/Box_Outplace.JPG").convert()
# Game_Success        =   pg.image.load("source/Success.jpg").convert()
# Image_Player        =   pg.image.load("source/man.jpg").convert()
# Image_Goal          =   pg.image.load("source/Goal.jpg").convert()
# Image_Wall          =   pg.image.load("source/wall.jpg").convert()
#
# # 截取所需图片大小
# Image_Help          =   pg.transform.scale(Image_Help,(BackgroundSize,BackgroundSize))
# Image_Welcome       =   pg.transform.scale(Image_Welcome,(BackgroundSize,BackgroundSize))
# Image_Box_Inplace   =   pg.transform.scale(Image_Box_Inplace,(Game_Map_Size,Game_Map_Size))
# Image_Box_Outplace  =   pg.transform.scale(Image_Box_Outplace,(Game_Map_Size,Game_Map_Size))
# Image_Player        =   pg.transform.scale(Image_Player,(Game_Map_Size,Game_Map_Size))
# Image_Wall          =   pg.transform.scale(Image_Wall,(Game_Map_Size,Game_Map_Size))
# Image_Goal          =   pg.transform.scale(Image_Goal,(Game_Map_Size,Game_Map_Size))
# Image_Game_Success  =   pg.transform.scale(Game_Success,(Game_Map_Size * 2,Game_Map_Size * 2))
#


class Portable(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self._pos = 0, 0

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        x, y = value
        self._pos = value
        self.rect.topleft = x * self.rect.width, y * self.rect.height

    def down(self):
        self.rect.center += vec(0, self.rect.height)

    def up(self):
        self.rect.center -= vec(0, self.rect.height)

    def left(self):
        self.rect.center -= vec(self.rect.width, 0)

    def right(self):
        self.rect.center += vec(self.rect.width, 0)


class Player(Portable):
    def __init__(self):
        self.image = pg.image.load("source/man.jpg").convert()
        self.image = pg.transform.scale(self.image ,(Game_Map_Size,Game_Map_Size))
        super().__init__()


class Box(Portable):
    def __init__(self, inplace=False):

        self.in_image = pg.image.load("source/Box_Inplace.jpg").convert()
        self.in_image = pg.transform.scale(self.in_image,(Game_Map_Size,Game_Map_Size))

        self.out_image = pg.image.load("source/Box_Outplace.JPG").convert()
        self.out_image = pg.transform.scale(self.out_image,(Game_Map_Size,Game_Map_Size))

        if inplace:
            self.image = self.in_image
        else:
            self.image = self.out_image
        super().__init__()


class Map(object):
    def __init__(self):
        # self._map = [[None] * MAX_STEP] * MAX_STEP
        self._map = []
        for i in range(MAX_STEP):
            row = []
            for j in range(MAX_STEP):
                row.append([])
            self._map.append(row)

    def get(self, x, y):
        try:
            return self._map[x][y]
        except KeyError:
            return None

    def load(self):
        self._map[0][2] = "P"
        self._map[0][3] = "B"
        self._map[1][3] = "B"
        self._map[3][3] = "B"

    def items(self):
        for x, items in enumerate(self._map):
            for y, item in enumerate(items):
                if item == 'P':
                    player = Player()
                    player.pos = (x, y)
                    yield player
                elif item == "B":
                    box = Box()
                    box.pos = (x, y)
                    yield box


class Game:

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((BackgroundSize,BackgroundSize),0,32)
        self.screen.fill((255,255,255))
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False
        self.all_sprites = None
        self.player = None
        self._box = None
        self._map = Map()


    def new(self):
        self.all_sprites = pg.sprite.Group()
        # 创建玩家实例，并加入容器
        self._map.load()
        for sprite in self._map.items():
            if isinstance(sprite, Player):
                self.player = sprite
            self.all_sprites.add(sprite)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(30)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.player.down()
                elif event.key == pg.K_UP:
                    self.player.up()
                elif event.key == pg.K_RIGHT:
                    self.player.right()
                elif event.key == pg.K_LEFT:
                    self.player.left()

    def draw(self):
        self.screen.fill((255,255,255))
        self.all_sprites.draw(self.screen)
        pg.display.update()


    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


def main():
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()

    pg.quit()


if __name__ == '__main__':
    main()
