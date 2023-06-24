import pygame
from settings import *
from enemy import Enemy
from support import *
from bomb import Bomb


class DarkLink(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_xp, create_bomb, spawn_rune):
        #general setup
        super().__init__('darklink', pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_xp, spawn_rune)
        self.sprite_type = 'enemy' #may need to change this and in YSortCameraGroup later
        monster_info = monster_data[self.monster_name]
        self.hitbox = self.rect.inflate(-100, -100)
        self.bomb_radius = monster_info['bomb_radius']
        self.bomb_time = None
        self.bomb_cooldown = 4000
        self.can_bomb = True
        self.can_attack = True
        self.create_bomb = create_bomb
        self.status = 'spawn'
        #self.spawn_rune = spawn_rune
        self.done_spawning = False

        


    def get_status(self, player):
        direction = self.get_player_distance_direction(player)[1]
        distance = self.get_player_distance_direction(player)[0]
        
        if direction.x > 0 and direction.x > direction.y:
            directionStr = 'right'
        elif direction.x <= 0 and direction.x < direction.y:
            directionStr = 'left'
        elif direction.y < 0:
            directionStr = 'up'
        else:
            directionStr = 'down'

        if '_' in self.status:
            action = self.status.split('_')[1]
            #print(action)
        else:
            action = ''


        if distance <= self.attack_radius and self.can_attack:
            if action != 'attack':
                self.frame_index = 0
            self.status = directionStr + '_attack'
        #Throw bomb
        elif distance <= self.bomb_radius and self.can_bomb:
            if action != 'bomb':
                self.frame_index = 0
                self.create_bomb(self, player)         
            self.status = directionStr + '_bomb'
            
        elif distance <= self.notice_radius:
            self.status = directionStr
        else:
            self.status = 'down_idle'

    def actions(self, player):
        if '_' in self.status:
            action = self.status.split('_')[1]
            #print(action)
        else:
            action = ''


        if action == 'attack':            
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'down_bomb': #TODO add bomb specific sounds and variables
            self.bomb_time = pygame.time.get_ticks()            
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
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
            #print(action)
        else:
            action = ''
        
        if self.frame_index >= len(animation):
            if action == 'attack':
                self.can_attack = False
            elif self.status == 'bomb':
                self.can_bomb = False
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

        if not self.can_bomb:
            if current_time - self.bomb_time >= self.bomb_cooldown:
                self.can_bomb = True

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()    
        self.check_death()      


    def enemy_update(self, player):     
        self.get_status(player)
        self.actions(player)