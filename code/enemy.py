import pygame
from settings import *
from entity import Entity
from support import *
from random import randint


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_xp, spawn_rune, spawn_health=None):
        #general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.spawned = False

        self.spawn_rune = spawn_rune
        #graphics setup
        self.import_graphics(monster_name)
        self.status = 'down_idle'
        self.image = self.animations[self.status][self.frame_index]

        #movement
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-50, -50) #probably the big hitbox problem
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_xp = add_xp

        if spawn_health != None:
            self.spawn_health = spawn_health

        #invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300


        #sounds
        self.death_sound = pygame.mixer.Sound('./audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('./audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])

        self.death_sound.set_volume(MAX_VOLUME)
        self.hit_sound.set_volume(MAX_VOLUME)
        self.attack_sound.set_volume(MAX_VOLUME)

    def import_graphics(self, name):
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
            'up_bomb':[], 'down_bomb':[], 'left_bomb':[], 'right_bomb':[], 
            'up_attack': [], 'down_attack':[], 'left_attack':[], 'right_attack':[],
            'spawn': [], 'down_fire':[], 'left_fire':[], 'right_fire':[], 'up_fire':[]}

        main_path = f'./graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation, name)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0,0)


        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'down_attack':
                self.frame_index = 0
            self.status = 'down_attack'
        elif distance <= self.notice_radius:
            self.status = 'down'
        else:
            self.status = 'down_idle'


    def actions(self, player):
        if self.status == 'down_attack':            
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'down':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'down_attack':
                self.can_attack = False
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

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            if not attack_type == 'explosion':
                self.hit_sound.play()
                self.direction = self.get_player_distance_direction(player)[1]
                if attack_type == 'weapon':
                    self.health -= player.get_full_weapon_damage()            
                elif attack_type == 'magic':
                    self.health -= player.get_full_magic_damage()
                self.hit_time = pygame.time.get_ticks()
                self.vulnerable = False


    def check_death(self):
        if self.health <= 0:
            if (self.monster_name == "darklink"):
                self.spawn_rune(self.rect.center)
            elif self.monster_name == "ganon":
                self.spawn_rune(self.rect.center, 8)
            elif randint(0, 3) == 1: #25% chance to drop health potion
                self.spawn_health(self.rect.center)
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            
            self.add_xp(self.exp)
            self.death_sound.play()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()    
        self.check_death()


    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)