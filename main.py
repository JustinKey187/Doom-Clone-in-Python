import pygame as pg
import sys
from pygame import mixer
from settings import *
from pygame.locals import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self): 
        pg.init()
        pg.mouse.set_visible(False)
        self.screen =  pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()
        pg.mixer.music.load("resources/audio/Pause_noise.mp3")
        pg.mixer.music.set_volume(1)
        pg.mixer.music.play(-1,0.0)

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        
    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

        keys = pg.key.get_pressed()
        if keys[pg.K_p]:
            self.pause_game()
    

    def pause_game(self):
        is_paused = True
        #pause loop
        pause_screen = pg.image.load("resources/ui/UI_Hands.png").convert_alpha()

        mixer.music.load("resources/audio/Pause_beat.mp3")
        mixer.music.set_volume(70)
        mixer.music.play()

        screen = pg.display.get_surface()
        clock = pg.time.Clock()
        while is_paused:
            screen.fill((0, 0, 0))
            screen.blit(pause_screen, (10, 10))
            pg.display.flip()
            clock.tick(30)

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        mixer.music.stop()
                        pg.mixer.music.load("resources/audio/Pause_noise.mp3")
                        pg.mixer.music.set_volume(1)
                        pg.mixer.music.play(-1,0.0)
                        is_paused = False

                if event.type == pg.QUIT:
                    is_paused = False
                    pg.quit()


        
    def draw(self):
      # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
      # self.map.draw()
      # self.player.draw()
        
    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)
                
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()