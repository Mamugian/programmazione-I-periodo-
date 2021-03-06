from actor import *
from game2d import *
from random import *

class Mario(Actor):
    W, H = 20, 26
    SPEED = 5

    def __init__(self, arena, x, y, synX, synY):
        self._x, self._y = x, y
        self._dx, self._dy = 0, 0
        self._synX, self._synY = synX, synY
        self._landed = False
        self._arena = arena
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()

        self._y += self._dy
        if self._y < 0:
            self._y = 0
        elif self._y > arena_h - self.H:
            self._y = arena_h - self.H
            self._landed = True

        if not self._landed:
            self._dy += 0.5
            
        self._x += self._dx       
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self.W:
            self._x = arena_w - self.W

    def go_left(self):
        self._dx, self._dy = -self.SPEED, 0
        
    def go_right(self):
        self._dx, self._dy = self.SPEED, 0

    def stay(self):
        self._dx, self._dy = 0, 0

    def collide(self, other):
        if  isinstance(other, Wall):
            x, y, w, h = other.rect()

            border_left = x - self.W
            border_right = x + w
            border_top =  y - self.H
            border_bottom = y + h

            if abs(border_left - self._x) < (border_right - self._x):
                nearest_x = border_left
            else:
                nearest_x = border_right
                
            if abs(border_top - self._y) < (border_bottom - self._y):
                nearest_y = border_top
            else:
                nearest_y = border_bottom

            if abs(nearest_x - self._x) < abs(nearest_y - self._y):
                self._x = nearest_x
##
##            elif isinstance(other, Goomba):
##            x, y, w, h = other.rect()
            
            else:
                self._y = nearest_y
        
    def rect(self):
        return self._x, self._y, self.W, self.H

    def symbol(self):
        return self._synX, self._synY

    def jump(self):
        if self._landed:
            self._dy = -self.SPEED * 2
            self._landed = False

##class Goomba(Actor):
##    W, H = 20, 26
##    SPEED = 3
##
##    def __init__(self, arena, x, y, synX, synY):
##        self._x, self._y = x, y
##        self._dx, self._dy = 0, 0
##        self._synX, self._synY = synX, synY
##        self._landed = False
##        self._arena = arena
##        arena.add(self)
##
##    def move(self):
##        arena_w, arena_h = self._arena.size()
##
##        self._y += self._dy
##        if self._y < 0:
##            self._y = 0
##        elif self._y > arena_h - self.H:
##            self._y = arena_h - self.H
##            self._landed = True
##
##        if not self._landed:
##            self._dy += 0.5
##            
##        self._x += self._dx       
##        if self._x < 0:
##            self._x = 0
##        elif self._x > arena_w - self.W:
##            self._x = arena_w - self.W
##
##    def collide(self, other):
##        if  isinstance(other, Wall):
##            x, y, w, h = other.rect()
##
##            border_left = x - self.W
##            border_right = x + w
##            border_top =  y - self.H
##            border_bottom = y + h
##
##            if abs(border_left - self._x) < (border_right - self._x):
##                nearest_x = border_left
##            else:
##                nearest_x = border_right
##                
##            if abs(border_top - self._y) < (border_bottom - self._y):
##                nearest_y = border_top
##            else:
##                nearest_y = border_bottom
##
##            if abs(nearest_x - self._x) < abs(nearest_y - self._y):
##                self._x = nearest_x
##            else:
##                self._y = nearest_y
##        
##    def rect(self):
##        return self._x, self._y, self.W, self.H
##
##    def symbol(self):
##        return self._synX, self._synY
##
##    def jump(self):
##        if self._landed:
##            self._dy = -self.SPEED * 2
##            self._landed = False



class Wall(Actor):

    def __init__(self, arena, x, y, w, h, synX, synY):
        self._x, self._y = x, y
        self._w, self._h = w, h
        self._synX, self._synY = synX, synY
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass
        
    def rect(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return self._synX, self._synY


def update():
    canvas_fill(canvas, (200, 200, 255))
    image_blit(canvas, terrain, (0, 230))

    for a in walls:
        x, y, w, h = a.rect()
        xs, ys = a.symbol()
        image_blit(canvas, sprites, (x, y), area = (xs, ys, w, h))
        
    arena.move_all()
    
    for a in arena.actors():
        x, y, w, h = a.rect()
        xs, ys = a.symbol()
        a_symbol = image_blit(canvas, sprites, (x, y), area = (xs, ys, w, h))


def print_arena(arena):
    for a in arena.actors():
        print(type(a).__name__, '@', a.rect())


def keydown(event):
    code = event.code
    if code == "ArrowRight":
        mario.go_right()
    elif code == "ArrowLeft":
        mario.go_left()
    elif code == "Space":
        mario.jump()

def keyup(event):
    code = event.code
    if code in ("ArrowLeft", "ArrowRight"):
        mario.stay()


arena = Arena(300, 240)
mario = Mario(arena, 10, 36, 210, 0)
walls = []
wall = Wall(arena, 150, 150, 20, 20, 5, 640)
walls.append(wall)
wall1 = Wall(arena, 240, 197, 35, 70, 309, 1167)
walls.append(wall1)

canvas = canvas_init((arena.size()))
sprites = image_load("smb_sprites.png")
terrain = image_load("terrain.png")

set_interval(update, 1000 // 30)

doc.onkeydown = keydown
doc.onkeyup = keyup
