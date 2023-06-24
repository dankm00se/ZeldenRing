from venv import create
import pygame
from settings import *
from support import *
from entity import Entity
from debug import debug
from random import randint

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/player/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-100, HITBOX_OFFSET['player'])
        

        #graphics setup
        self.import_player_assets()
        self.status = 'down'

        #movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0
        self.can_move = True
        

        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.attack_type = "none"
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        #runes
        self.runes = 0

        self.potions = 5
        self.healing = False
        self.healing_time = None
        self.heal_cooldown = 500

        #magic
        #TODO Change this to bomb throwing, and healing potions
        '''
        self.magicking = False
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        '''
        self.can_switch_items = True
        self.item_switch_time = None

        #stats
        self.stats = {'health': 100, 'energy':60, 'attack':10, 'magic': 4, 'speed': 6}
        self.max_stats = {'health': 300, 'energy':140, 'attack':20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy':100, 'attack':100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 500

        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        #import sounds
        self.weapon_attack_sound = pygame.mixer.Sound('./audio/sword.wav')
        self.weapon_attack_sound.set_volume(MAX_VOLUME)

        self.heal_sound = pygame.mixer.Sound('./audio/heal.wav')
        self.heal_sound.set_volume(MAX_VOLUME)

        self.death_sound = pygame.mixer.Sound('./audio/zelda/death_5_karen.wav')
        self.death_sound.set_volume(MAX_VOLUME)

        self.grunting_sounds = [pygame.mixer.Sound('./audio/zelda/grunting_5_karen.wav'), pygame.mixer.Sound('./audio/zelda/grunting_7_karen.wav')]
        self.grunting_sounds[0].set_volume(MAX_VOLUME)
        self.grunting_sounds[1].set_volume(MAX_VOLUME)

        self.hurt_sound_played = False

        self.damaged_sounds = [pygame.mixer.Sound('./audio/zelda/damaged1.wav'), pygame.mixer.Sound('./audio/zelda/damaged2.wav'), pygame.mixer.Sound('./audio/zelda/damaged3.wav')]
        for i in range(len(self.damaged_sounds)):
            self.damaged_sounds[i].set_volume(MAX_VOLUME * 4)
    
    def import_player_assets(self):
        character_path = './graphics/player/'
        #change magic to bombs
        self.animations = {
            'up':[], 'down':[], 'left':[], 'right':[],
            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
            'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[],
            'up_magic':[], 'down_magic':[], 'left_magic':[], 'right_magic':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation           
            self.animations[animation] = import_folder(full_path, "player")
        


    def input(self):
        keys = pygame.key.get_pressed()

                                #and not self.magickng
        if not self.attacking and self.can_move:
            #movement input
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            #attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.grunting_sounds[randint(0,1)].play()
                self.create_attack()
                self.weapon_attack_sound.play()

            #heal input
            if keys[pygame.K_LCTRL]:
                if self.potions > 0 and not self.healing and self.health < 100:
                    self.healing = True
                    self.healing_time = pygame.time.get_ticks()
                    self.potions -= 1
                    self.health += 50

                    self.heal_sound.play()

                    if self.health > 100:
                        self.health = 100

            '''
                self.magicking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)
            '''
            #weapon switch
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index = (self.weapon_index + 1) % len(list(weapon_data.keys()))
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            #item switch
            if keys[pygame.K_e] and self.can_switch_items:
                self.can_switch_items = False
                self.item_switch_time = pygame.time.get_ticks()
                #self.magic_index = (self.magic_index + 1) % len(list(magic_data.keys()))
                #self.magic = list(magic_data.keys())[self.magic_index]
    
    def get_status(self):

        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status and not 'magic' in self.status:
                self.status = self.status + '_idle'
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
        '''
        if self.magicking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'magic' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_magic')
                else:
                    self.status = self.status + '_magic'
        else:
            if 'magic' in self.status:
                self.status = self.status.replace('_magic', '')
        '''


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
        
        '''
        if self.magicking:
            if current_time - self.attack_time >= self.attack_cooldown + magic_data[self.magic]['cooldown']:
                self.magicking = False            
        '''

        if self.healing:
            if current_time - self.healing_time >= self.heal_cooldown:
                self.healing = False
        
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True               
        
        if not self.can_switch_items:
            if current_time - self.item_switch_time >= self.switch_duration_cooldown:
                self.can_switch_items = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
                self.hurt_sound_played = False
            elif not self.hurt_sound_played:
                self.damaged_sounds[randint(0, 2)].play()
                self.hurt_sound_played = True
                
    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
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

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic'] #so we can level up magic abilities
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()        
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
        



   