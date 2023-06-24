import pygame
from debug import debug
from level import *
from support import *
from settings import *
from rune import Rune
from oldman import OldMan
import math


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2        
        self.offset = pygame.math.Vector2()

        #creating the floor
        #self.floor_surf = pygame.image.load("./graphics/tilemap/something.png").convert()
        self.floor_surf = pygame.image.load("./graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0 - TILESIZE))

        #spawning
        self.spawn_left = False
        self.spawn_top = False
        self.spawn_right = False        

        self.end_time = None

        self.left_glow_done = False
        self.right_glow_done = False
        self.mid_glow_done = False


    def custom_draw(self, player, context=''):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        oldman = None
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset            
            self.display_surface.blit(sprite.image, offset_pos)
            if(type(sprite) == OldMan):
                oldman = sprite
        #display dialogue last so that it shows on top of everything 
        if math.dist(player.rect.center, oldman.rect.center) <= 50:
            if oldman.showing_dialogue:
                oldman.show_dialogue(context)
            else:
                oldman.show_key(self.display_surface, oldman.rect.topleft - self.offset)

    def check_if_blue_glow(self, level):
        if level.player.runes == 3 and not self.left_glow_done:
            for sprite in self.sprites():
                if sprite.rect.centerx < 1000:
                    sprite.remove(level.conditional_sprites)
                    sprite.groups().append(level.visible_sprites)
                    sprite.sprite_type = 'wall'
                #print(sprite.groups)
            self.left_glow_done = True
            
        if level.player.runes == 5 and not self.right_glow_done:
            for sprite in self.sprites():
                if sprite.rect.centerx > 1800:
                    sprite.groups = [level.visible_sprites]
                    sprite.sprite_type = 'wall'
                    sprite.remove(level.conditional_sprites)
            self.right_glow_done = True
        if level.player.runes == 8 and (not self.right_glow_done or not self.left_glow_done):
            for sprite in self.sprites():
                if sprite.rect.centerx < 1000 or sprite.rect.centerx > 1800:
                    sprite.groups = [level.visible_sprites]
                    sprite.sprite_type = 'wall'
                    sprite.remove(level.conditional_sprites)
            self.right_glow_done = True
            self.left_glow_done = True
        if level.player.runes == 16 and (not self.right_glow_done or not self.left_glow_done or not self.mid_glow_done):
            for sprite in self.sprites():
                sprite.groups = [level.visible_sprites]
                sprite.sprite_type = 'wall'
            
            self.right_glow_done = True
            self.left_glow_done = True
            self.mid_glow_done = True

            
        
    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        bomb_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'bomb']
        fire_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'flame']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
        for bomb in bomb_sprites:
            bomb.update()
            if bomb.is_exploding:
                player_pos = player.rect.center
                bomb_pos = bomb.rect.center
                dist = math.dist(player_pos, bomb_pos)
                if dist < 64 and not bomb.damaged_player:
                    bomb.damage_player(bomb.attack_damage, bomb.attack_type)
                    bomb.damaged_player = True
        for fire in fire_sprites:
            fire.update()

    def play_left_cutscene(self, level):
        current_time = pygame.time.get_ticks()
        move_time = 2000
        stop_time = 7000
        
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        if self.offset.x < 110 and self.offset.x > 90 and not level.spawn_left_done:
            self.spawn_left = True
        elif self.offset.x > 100 and not level.spawn_left_done:
            self.offset.x -= 1        
            self.end_time = pygame.time.get_ticks()

        if self.spawn_left:
            #print("spawning now")            
            level.spawn_left = True
            
        if level.spawn_left_done and current_time - self.end_time >= move_time:        
            #print("adding one")    
            self.offset.x += 1
            if current_time - self.end_time >= stop_time:
                level.left_cutscene_done = True
                return False
        
        return True
    
    def play_right_cutscene(self, level):
        current_time = pygame.time.get_ticks()
        move_time = 2000
        stop_time = 7000
        
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        if self.offset.x < 2200 and self.offset.x > 2190 and not level.spawn_right_done:
            self.spawn_right = True
        elif self.offset.x < 2200 and not level.spawn_right_done:
            self.offset.x += 1        
            self.end_time = pygame.time.get_ticks()

        #print(self.offset.x)
        if self.spawn_right:
            #print("spawning now")            
            level.spawn_right = True
            
        if level.spawn_right_done and current_time - self.end_time >= move_time:        
            #print("adding one")    
            self.offset.x -= 1
            if current_time - self.end_time >= stop_time:
                level.right_cutscene_done = True
                return False
        
        return True
    
    def play_top_cutscene(self, level):
        current_time = pygame.time.get_ticks()
        move_time = 2000
        stop_time = 7000
        
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        if self.offset.y < 335 and self.offset.y > 330 and not level.spawn_top_done:
            self.spawn_top = True
        elif self.offset.y > 330 and not level.spawn_top_done:
            self.offset.y -= 1        
            self.end_time = pygame.time.get_ticks()

        #print(self.offset.y)

        if self.spawn_top:
            #print("spawning ganon")            
            level.spawn_top = True
            
        if level.spawn_top_done and current_time - self.end_time >= move_time:        
           #print("adding one")    
            self.offset.y += 1
            if current_time - self.end_time >= stop_time:
                level.top_cutscene_done = True
                return False
        
        return True