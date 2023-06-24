import pygame

from support import *
from settings import *
from particles import AnimationPlayer
import math


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, entity, trigger_explosion_particles, player, damage_player):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/weapons/bomb/bomb1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft = pos)
        self.dest_pos = pygame.math.Vector2(player.rect.center)
        self.cur_pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.Vector2()
        self.speed = 2
        self.sprite_type = 'bomb'
        self.detonate_timer = 1500
        self.countdown_timer = pygame.time.get_ticks()
        self.attack_type = 'explosion'
        self.attack_damage = 40
        self.trigger_explosion_particles = trigger_explosion_particles
        self.is_exploding = False
        self.damaged_player = False
        self.damage_player = damage_player

        self.explode_sound = pygame.mixer.Sound('./audio/bomb/explode.wav')
        self.explode_sound.set_volume(MAX_VOLUME)


        direction = entity.status.split('_')[0]

        #animations
        self.import_bomb_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        
        #placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = entity.rect.midright + pygame.math.Vector2(-30, 48))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = entity.rect.midleft + pygame.math.Vector2(30, 48))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = entity.rect.midbottom + pygame.math.Vector2(-30, 0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = entity.rect.midtop + pygame.math.Vector2(-30, 0))
        else:
            self.rect = self.image.get_rect(center = entity.rect.center)

    def import_bomb_assets(self):
        bomb_path = './graphics/weapons/bomb/'
        self.animations = import_folder(bomb_path, "bomb")
    
    def countdown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.countdown_timer >= self.detonate_timer:
            self.detonate()            
        if current_time - self.countdown_timer >= self.detonate_timer * 2:
            self.kill()


    def get_damage(self, player, attack_type):
        pass #only here because of level.py player_attack_logic
    
    def detonate(self):
        
        self.trigger_explosion_particles(self.rect.center, self.sprite_type)
        if not self.is_exploding:
            self.explode_sound.play()
        self.is_exploding = True
        

    def move(self):
        distance = math.dist(self.dest_pos, self.cur_pos)
        #if distance > 64:
        current_time = pygame.time.get_ticks()
        self.direction = pygame.Vector2.normalize(self.dest_pos - self.cur_pos)
        #if current_time - self.countdown_timer <= 500:
        if distance > 32:
            self.cur_pos += self.direction * self.speed
            self.rect.center = self.cur_pos


    def animate(self):
        #animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        
        #set the image
        self.image = self.animations[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(center = self.rect.center)


    def update(self):
        self.countdown()
        self.move()
        self.animate()

