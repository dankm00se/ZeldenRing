import pygame

import moviepy.editor
from pygame import Rect
from settings import *
from tile import Tile
from player import Player
from darklink import DarkLink
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from random import randint
import math
from bomb import Bomb
from fire import Fire
from ganon import Ganon
from ysortcameragroup import YSortCameraGroup
from rune import Rune
from dialogue import Dialogue
from oldman import OldMan
from health import Health


class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # Sprite Group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #Trigger sprites
        self.triggerleft_sprites = pygame.sprite.Group()
        self.triggerright_sprites = pygame.sprite.Group()
        self.triggermid_sprites = pygame.sprite.Group()
        self.triggertop_sprites = pygame.sprite.Group()

        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #blue decals
        self.conditional_sprites = YSortCameraGroup()

        #random monsters to pick from
        self.random_monsters = ['bamboo', 'spirit', 'squid', 'biri']

        #spawning variables
        self.spawn_left = False
        self.spawn_left_done = False

        self.spawn_top = False
        self.spawn_top_done = False

        self.spawn_right = False
        self.spawn_right_done = False

        #enemy groups
        self.left_group = list()        

        self.top_group = list()

        self.right_group = list()

        #sprite setup
        self.create_map()

        self.dead = False
        #user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
            
        self.right_glow_done = False
        self.left_glow_done = False
        self.mid_glow_done = False

        #cutscene variables
        self.play_left_cutscene = False
        self.play_right_cutscene = False
        self.play_top_cutscene = False
        self.play_mid_cutscene = False

        self.left_cutscene_done = False
        self.right_cutscene_done = False
        self.top_cutscene_done = False
        self.mid_cutscene_done = False

        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        #sounds
        self.game_over_sound = pygame.mixer.Sound('./audio/gameover.wav')
        self.game_over_sound.set_volume(MAX_VOLUME)

        self.progress_sound = pygame.mixer.Sound('./audio/progress.wav')
        self.progress_sound.set_volume(MAX_VOLUME * 2)

        self.victory_sound = pygame.mixer.Sound('./audio/progress.wav')
        self.victory_sound.set_volume(MAX_VOLUME * 2)

        self.spawn_sound = pygame.mixer.Sound('./audio/spawn.wav')
        self.spawn_sound.set_volume(MAX_VOLUME * 2)
        
        #dialogue test
        self.dialogue = Dialogue()
        self.context_str = ''

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./map/Ancient Meadow_Boundary.csv'),
            'trees': import_csv_layout('./map/Ancient Meadow_Trees.csv'),            
            'wall': import_csv_layout('./map/Ancient Meadow_Walls.csv'),
            'props' : import_csv_layout('./map/Ancient Meadow_Props.csv'),
            'entities' : import_csv_layout('./map/Ancient Meadow_Entities.csv'),
            'objectDetails' : import_csv_layout('./map/Ancient Meadow_ObjectDetails.csv'),
            'breakables': import_csv_layout('./map/Ancient Meadow_Breakables.csv'),
            'triggerleft' : import_csv_layout('./map/Ancient Meadow_TriggerLeft.csv'),
            'triggerright' : import_csv_layout('./map/Ancient Meadow_TriggerRight.csv'),
            'triggermid' : import_csv_layout('./map/Ancient Meadow_TriggerMid.csv'),
            'triggertop' : import_csv_layout('./map/Ancient Meadow_TriggerTop.csv')
        }
        graphics = {
            'trees': import_folder('./graphics/trees'),
            'walls': import_folder('./graphics/walls'),
            'objectDetails' : import_folder('./graphics/objectdetails'),
            'props' : import_folder('./graphics/props')
        }
        for style, layout in layouts.items():            
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                                                

                        if style == 'boundary':
                            surf = pygame.image.load('./graphics/entities/61.png').convert_alpha()
                            #Tile((x,y), [self.obstacle_sprites], 'invisible', surf)
                        if style == 'grass':
                            #create a grass tile
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x,y),
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                'grass',
                                random_grass_image) 
                        if style == 'trees':
                            surf = graphics['trees'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'wall', surf)
                        if style == 'wall':
                            #create a wall tile
                            surf = graphics['walls'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'wall', surf)                                               
                            #Tile((x,y), [self.obstacle_sprites], 'wall', surf)
                        if style == 'breakables':
                            surf = graphics['props'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'breakable', surf)
                        if style == 'objectDetails':
                            surf = graphics['objectDetails'][int(col)]                                                                   
                            if (int(col) == 56 or int(col) == 24 or int(col) == 72 or int(col) == 104 or int(col) == 138):
                                Tile((x,y), [self.conditional_sprites], 'invisible', surf)
                            else:
                                Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'wall', surf)


                        if style == 'props':
                            surf = graphics['props'][int(col)]  
                            if (int(col) == 39):
                                Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'pillar', surf)
                            else:
                                Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'wall', surf)

                        #various triggers that will spawn enemies in 
                        if style == 'triggerleft':
                            surf = pygame.image.load('./graphics/entities/61.png').convert_alpha()
                            Tile((x,y), [self.triggerleft_sprites], 'trigger', surf)
                        
                        if style == 'triggerright':
                            surf = pygame.image.load('./graphics/entities/61.png').convert_alpha()
                            Tile((x,y), [self.triggerright_sprites], 'trigger', surf)

                        if style == 'triggermid':
                            surf = pygame.image.load('./graphics/entities/61.png').convert_alpha()
                            Tile((x,y), [self.triggermid_sprites], 'trigger', surf)

                        if style == 'triggertop':
                            surf = pygame.image.load('./graphics/entities/61.png').convert_alpha()
                            Tile((x,y), [self.triggertop_sprites], 'trigger', surf)
                        
                        
                                                                     

                        if style == 'entities':
                            if col == '64': #Player start is 64
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack,
                                    self.create_magic)
                            elif col == '39':#Oldman
                                self.oldman = OldMan(
                                    (x,y),
                                    [self.visible_sprites])
                            else:
                                if col=='65':  #GANON - Need to add support for Ganon
                                  
                                    self.top_group.append((x,y))
                                elif col=='66' :
                                    monster_name ='darklink'
                                    if x < 1000:
                                        self.left_group.append((x,y))
                                    elif x > 2000:
                                        self.right_group.append((x,y))
                                        
                                elif col=='67': #random
                                    monster_name = self.random_monsters[randint(0, len(self.random_monsters) - 1)]
                                    Enemy(
                                        monster_name, 
                                        (x, y), 
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles,
                                        self.add_xp,
                                        self.spawn_rune,
                                        self.spawn_health_potion)
        


        
    def create_attack(self):
        #self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
        self.player.rect = self.player.rect.inflate(-100, -100)
        self.attack_sprites.add(self.player)
        self.player.attack_type = "weapon"

    def play_video(self):
        video = moviepy.editor.VideoFileClip("./video/propose_noname.mp4")
        video.preview()
        

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        elif style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
                
    def create_bomb(self, entity, player):
        bomb = Bomb(entity.rect.center, [self.visible_sprites], entity, self.trigger_explosion_particles, player, self.damage_player)
        self.attack_sprites.add(bomb)

    def create_fire(self, entity, player, position_offset=None):
        fire = Fire(entity.rect.center, [self.visible_sprites], entity, self.trigger_fire_particles, player, self.damage_player)
        self.attack_sprites.add(fire)

    def destroy_attack(self):
        #if self.current_attack:
        #    self.current_attack.kill()
        #self.current_attack = None
        self.attack_sprites.remove(self.player)
        self.player.attack_type = "none"

    def colliding_sprites(self, attack_sprite, group):
        return [
            group_sprite
            for group_sprite in group
            if attack_sprite.rect.colliderect(group_sprite.rect)
            
        ]
    #TODO FIX COLLISION!! The player should be colliding with the enemy in order to attack, right now the player is too far away when attacking.
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                is_player = False
                if type(attack_sprite) == Player:
                    is_player = True
                collision_sprites = []
                for attackable_sprite in self.attackable_sprites:
                    #if the attacking sprite is the player, then handle the player attacking an enemy
                    #TODO: add player functionality to bomb // shouldn't friendly fire
                    #TODO: add a little distance in the direction the player is facing so they can attack from a bit further away
                    #TODO: make check for fire sprite
                    if is_player:
                        enemy_vec = pygame.math.Vector2(attackable_sprite.rect.center)                    
                        player_vec = pygame.math.Vector2(attack_sprite.rect.center)



                        distance = math.dist(player_vec,enemy_vec)
                        if distance <= attackable_sprite.rect.size[1] / 2 + 15:                            
                            # collision_sprites = [
                            #     group_sprite
                            #     for group_sprite in self.attackable_sprites
                            #     if attack_sprite.rect.colliderect(group_sprite.rect)
                            #     ]
                            collision_sprites.append(attackable_sprite)
                    else:
                        #print('fire fire fire')
                        if math.dist(self.player.rect.center, attack_sprite.rect.center) < 32:
                            collision_sprites.append(attack_sprite)

                #collision_sprites = self.colliding_sprites(attack_sprite, self.attackable_sprites)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        elif target_sprite.sprite_type == 'flame':                            
                            self.damage_player(target_sprite.get_damage(self.player, 'fire'), 'flame')
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.attack_type)
    #checking the various triggers to play cutscenes
    def check_trigger_collision(self, player):
        #trigger_sprites = [self.triggerleft_sprites, self.triggerright_sprites, self.triggermid_sprites, self.triggertop_sprites]
        trigger_sprites = [self.triggerleft_sprites]
        for group in trigger_sprites:
            for trigger in group:
                if math.dist(trigger.rect.center, player.rect.center) < 32:
                    self.play_left_cutscene = True

        trigger_sprites = [self.triggerright_sprites]
        for group in trigger_sprites:
                for trigger in group:
                    if math.dist(trigger.rect.center, player.rect.center) < 32:
                        self.play_right_cutscene = True

        trigger_sprites = [self.triggertop_sprites]
        for group in trigger_sprites:
            for trigger in group:
                if math.dist(trigger.rect.center, player.rect.center) < 32:
                    if self.left_cutscene_done and self.right_cutscene_done:
                        self.play_top_cutscene = True

        keys = pygame.key.get_pressed()
        trigger_sprites = [self.triggermid_sprites]
        for group in trigger_sprites:
            for trigger in group:
                if math.dist(trigger.rect.center, player.rect.center) < 16 and keys[pygame.K_e] and self.spawn_left_done and self.spawn_right_done and self.spawn_top_done and self.player.runes == 16:
                    
                    self.play_video()
        

    def spawn_enemies(self, group):
        if group == 'left' and not self.spawn_left_done:
            for pos in self.left_group:
                DarkLink( 
                    pos, 
                    [self.visible_sprites, self.attackable_sprites],
                    self.obstacle_sprites,
                    self.damage_player,
                    self.trigger_death_particles,
                    self.add_xp,
                    self.create_bomb,
                    self.spawn_rune)
            self.spawn_left_done = True
        #spawning ganon
        if group == 'top' and not self.spawn_top_done:
            for pos in self.top_group:                
                Ganon(pos,
                    [self.visible_sprites, self.attackable_sprites],
                    self.obstacle_sprites,
                    self.damage_player,
                    self.trigger_death_particles,
                    self.add_xp,
                    self.create_fire,
                    self.spawn_rune)
                self.spawn_sound.play()
            self.spawn_top_done = True
        
        if group == 'right' and not self.spawn_right_done:
            for pos in self.right_group:
                DarkLink( 
                    pos, 
                    [self.visible_sprites, self.attackable_sprites],
                    self.obstacle_sprites,
                    self.damage_player,
                    self.trigger_death_particles,
                    self.add_xp,
                    self.create_bomb,
                    self.spawn_rune)
            self.spawn_right_done = True
    def spawn_rune(self, pos, amount=1):
        if amount == 1:
            Rune([self.visible_sprites], pos)
        else:
            for i in range(amount):
                Rune([self.visible_sprites], (pos[0] + randint(-30, 30), pos[1] + randint(-30, 30)))

    def spawn_health_potion(self, pos):
        Health([self.visible_sprites], pos)

    
    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #spawn particles based on attack_type
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
        
    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def trigger_explosion_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def trigger_fire_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)
    def add_xp(self, amount):
        self.player.exp += amount

    def check_oldman(self, player):
        keys = pygame.key.get_pressed()

        if math.dist(player.rect.center, self.oldman.rect.center) < 40 and keys[pygame.K_e]:
            self.context_str = ''
            #this is flawed because it only checks if the enemies are spawned, not if they're killed
            if not self.spawn_left_done:
                self.context_str += 'l'
            if not self.spawn_right_done:
                self.context_str += 'r'
            if not self.spawn_top_done:
                self.context_str += 't'
            #self.oldman.show_dialogue(self.context_str)
            self.oldman.showing_dialogue = True
            self.game_paused = True
        #elif math.dist(player.rect.center, self.oldman.rect.center) < 40:
            #self.oldman.show_key(self.display_surface)
            #print('displaying')

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def check_if_blue_glow(self):
        if self.player.runes == 3 and not self.left_glow_done and self.left_cutscene_done:
            for sprite in self.conditional_sprites.sprites():
                if sprite.rect.centerx < 1000:
                    sprite.remove(self.conditional_sprites)                                        
                    Tile(sprite.rect.topleft, [self.visible_sprites], 'wall', sprite.image)                
            self.left_glow_done = True
            self.progress_sound.play()
            
        if (self.player.runes == 5 and not self.right_glow_done and not self.left_glow_done) and self.right_cutscene_done:
            for sprite in self.conditional_sprites.sprites():
                if sprite.rect.centerx > 1800:
                    sprite.remove(self.conditional_sprites)
                    Tile(sprite.rect.topleft, [self.visible_sprites], 'wall', sprite.image)  
            self.right_glow_done = True
            self.progress_sound.play()
        if self.player.runes == 8 and (not self.right_glow_done or not self.left_glow_done):
            for sprite in self.conditional_sprites.sprites():
                if sprite.rect.centerx < 1000 or sprite.rect.centerx > 1800:
                    sprite.remove(self.conditional_sprites)
                    Tile(sprite.rect.topleft, [self.visible_sprites], 'wall', sprite.image)  
            self.right_glow_done = True
            self.left_glow_done = True
            self.progress_sound.play()
        if self.player.runes == 16 and (not self.right_glow_done or not self.left_glow_done or not self.mid_glow_done):
            for sprite in self.conditional_sprites.sprites():
                sprite.remove(self.conditional_sprites)
                Tile(sprite.rect.topleft, [self.visible_sprites], 'wall', sprite.image)  
            
            self.right_glow_done = True
            self.left_glow_done = True
            self.mid_glow_done = True
            self.victory_sound.play()

    def run(self):

        #self.visible_sprites.custom_draw(self.player)
        if self.oldman.showing_dialogue:            
            self.visible_sprites.custom_draw(self.player, self.context_str)

            if pygame.mouse.get_pressed()[0] and self.oldman.showing_dialogue:
                self.game_paused = False
                self.oldman.showing_dialogue = False
        
        elif self.game_paused:
            self.visible_sprites.custom_draw(self.player)


        elif self.play_left_cutscene and not self.left_cutscene_done:
            
            self.play_left_cutscene = self.visible_sprites.play_left_cutscene(self)
            self.visible_sprites.update()
            self.player.can_move = not self.play_left_cutscene
            self.player.direction = pygame.Vector2()
            if self.spawn_left:                
                self.spawn_enemies('left')

        elif self.play_right_cutscene and not self.right_cutscene_done:
 
            self.play_right_cutscene = self.visible_sprites.play_right_cutscene(self)
            self.visible_sprites.update()
            self.player.can_move = not self.play_right_cutscene
            self.player.direction = pygame.Vector2()
            if self.spawn_right:                
                self.spawn_enemies('right')
        
        elif self.play_top_cutscene and not self.top_cutscene_done:
            self.play_top_cutscene = self.visible_sprites.play_top_cutscene(self)
            self.visible_sprites.update()
            self.player.can_move = not self.play_top_cutscene
            self.player.direction = pygame.Vector2()
            if self.spawn_top:
                self.spawn_enemies('top')
        
        elif self.player.health <= 0:
            self.visible_sprites.custom_draw(self.player)
            #print(self.dead)
            if not self.dead:
                self.player.death_sound.play()
                pygame.time.wait(int(self.player.death_sound.get_length() * 1000))
                self.game_over_sound.play()
                
                self.dead = True
            done = self.ui.show_game_over()            

            if done:
                pygame.quit()
            

        else:
            self.visible_sprites.custom_draw(self.player)
            
            # update and draw the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
             
            self.check_trigger_collision(self.player)  
            self.check_oldman(self.player)
            self.player_attack_logic()

        self.check_if_blue_glow()

        #needs to be after everything so the ui can be on top of everything
        if self.player.health > 0:
            self.ui.display(self.player)

'''runes 
   W x 1
   I x 1
   L x 2
   Y x 2
   O x 1
   U x 1
   M x 2 
   A x 1
   R x 2
   E x 1
   ? x 1
      15
'''