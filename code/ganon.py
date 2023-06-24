import pygame
from settings import *
from enemy import Enemy
from support import *
from bomb import Bomb


class Ganon(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_xp, create_fire, spawn_rune):
        #general setup
        super().__init__('ganon', pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_xp, spawn_rune)
        self.sprite_type = 'enemy' #may need to change this and in YSortCameraGroup later
        monster_info = monster_data[self.monster_name]
        self.fire_radius = monster_info['fire_radius']
        self.hitbox = self.rect.inflate(-100, -100)
        self.fire_time = None
        self.max_fire_time = 1000
        self.fire_cooldown = 5000
        self.fire_damage = 3
        self.breathing_fire = False
        self.can_fire = True
        self.fire_interval = False
        self.can_attack = True
        self.create_fire = create_fire
        self.last_fire = None
        self.status = 'spawn'
        self.fire_sound = pygame.mixer.Sound('./audio/Fire.wav')
        self.fire_sound.set_volume(MAX_VOLUME)
        self.breathing_sound = pygame.mixer.Sound('./audio/ganon/heavyattack2.wav')
        self.breathing_sound.set_volume(MAX_VOLUME)
        self.death_sound = pygame.mixer.Sound('./audio/ganon/nooooo.wav')
        self.death_sound.set_volume(MAX_VOLUME * 3)
        self.death_sound.fadeout(1)        
        self.hit_sound = pygame.mixer.Sound('./audio/ganon/angry3.wav')
        self.hit_sound.set_volume(MAX_VOLUME)
        self.speed = 2
        self.done_spawning = False

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        if not self.breathing_fire:
            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')

            self.hitbox.y += self.direction.y * speed
            self.collision('vertical')
            
            self.rect.center = self.hitbox.center
        


    def get_status(self, player):
        direction = self.get_player_distance_direction(player)[1]
        distance = self.get_player_distance_direction(player)[0]
        
        if not self.breathing_fire:
            if direction.x > 0 and direction.x > direction.y:
                directionStr = 'right'
            elif direction.x <= 0 and direction.x < direction.y:
                directionStr = 'left'
            elif direction.y < 0:
                directionStr = 'up'
            else:
                directionStr = 'down'
        else:
            directionStr = self.status.split('_')[0]
                

        if '_' in self.status:
            action = self.status.split('_')[1]            
        else:
            action = ''

        #melee attack
        if distance <= self.attack_radius and self.can_attack:
            if action != 'attack':
                self.frame_index = 0
            self.status = directionStr + '_attack'
        #Shoot fire
        elif distance <= self.fire_radius and self.can_fire and self.can_attack:
            if action != 'fire' :
                self.frame_index = 0
                self.create_fire(self, player)
                self.fire_sound.play()
                self.last_fire = pygame.time.get_ticks()
                    
            self.status = directionStr + '_fire'
            self.can_fire = False
            self.breathing_fire = True
            self.fire_time = pygame.time.get_ticks()
        #breathing fire duration
        elif self.breathing_fire and self.fire_interval:
            self.create_fire(self, player)
            self.fire_sound.play()
            self.last_fire = pygame.time.get_ticks()
            self.fire_interval = False
            self.status = directionStr + '_fire'
        elif self.breathing_fire:
            self.status = directionStr + '_fire'
        elif distance <= self.notice_radius:
            self.status = directionStr
        else:
            self.status = 'down_idle'

         
    def actions(self, player):
        if '_' in self.status:
            action = self.status.split('_')[1]            
        else:
            action = ''

        if action == 'attack':            
            #sometimes attack_time can be "None" which results in the game crashing... FIX
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif action == 'fire': #TODO add fire specific sounds and variables
            #self.fire_time = pygame.time.get_ticks()
            #self.damage_player(self.fire_damage, "flame")
            #self.attack_sound.play()
            self.breathing_sound.play()
            pass
        elif self.status == 'down':
            self.direction = self.get_player_distance_direction(player)[1]
        elif self.status == 'up':
            self.direction = self.get_player_distance_direction(player)[1]
        elif self.status == 'left':
            self.direction = self.get_player_distance_direction(player)[1]
        elif self.status == 'right':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if '_' in self.status:
            action = self.status.split('_')[1]            
        else:
            action = ''
        
        if self.frame_index >= len(animation):
            if action == 'attack':
                self.can_attack = False
            elif action == 'fire':
                self.can_fire = False
            elif self.status == 'spawn':
                self.status = 'down_idle'
                self.done_spawning = True                
            self.frame_index = 0
        
        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

        if not self.can_fire:
            if current_time - self.fire_time >= self.fire_cooldown:
                self.can_fire = True

        if self.breathing_fire:
            if current_time - self.last_fire >= 60:
                self.fire_interval = True
            if current_time - self.fire_time >= self.max_fire_time:
                self.breathing_fire = False

        
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()    
        self.check_death()      


    def enemy_update(self, player):     
        self.get_status(player)
        self.actions(player)