import pygame
from player import Player
from math import sin
from support import *

class Rune(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        
        self.visible_sprites = groups[0]

        self.pickup_sound = pygame.mixer.Sound('./audio/rune/pickup.wav')
        self.pickup_sound.set_volume(0.25) #Make sure to remove the 0 later 

        self.import_graphics()
        self.image = self.animations['idle'][0]
        #self.image = pygame.image.load(f'Z:/Code/Zelden Ring/graphics/rune/1.png').convert_alpha()        
        #self.image = pygame.transform.scale(self.image, (32, 32))
        
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-20, -20)

        #check to make sure this wasn't added already
        self.added = False
        
    def move(self, speed=0):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision()

        self.hitbox.y += self.direction.y * speed
        self.collision()

        self.rect.center = self.hitbox.center
    
    def collision(self):
        for sprite in self.visible_sprites:
            if(type(sprite) == Player):
                if sprite.hitbox.colliderect(self.hitbox) and not self.added:
                    #if it's a player, add 1 to runes for the player and commit neckrope                    
                    sprite.runes += 1
                    self.added = True
                    self.pickup_sound.play()
                    self.kill()

    def import_graphics(self):
        self.animations = {'idle':[]}
        main_path = f'./graphics/rune/'
        
        self.animations['idle'] = import_folder(main_path)

    def animate(self):
            #animation = self.animations[self.status]

            #loop over the frame index
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.animations['idle']):
                self.frame_index = 0
            
            #set the image
            self.image = self.animations['idle'][int(self.frame_index)]       
            self.rect = self.image.get_rect(center = self.rect.center)


    def update(self):        
        self.move()
        self.animate()