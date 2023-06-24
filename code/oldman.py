import pygame
from settings import *
from entity import Entity
from support import *
from dialogue import Dialogue

class OldMan(Entity):
    def __init__(self, pos, groups):
        #general setup
        super().__init__(groups)
        self.sprite_type = 'oldman'
        self.spawned = False
        self.showing_dialogue = False
        
        #graphics setup
        self.import_graphics()
        self.import_key_graphics()
        self.status = 'down_idle'
        self.image = self.animations[self.status][self.frame_index]
        self.key_image = self.key_animations['e'][0]

        self.key_animation_speed = 0.02
        self.key_frame_index = 0

        #movement
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-100, -100)
        self.speed = 2

        #sounds        
        self.grunt_sound = pygame.mixer.Sound('./audio/oldman/grunting_2_alex.wav') # add real sound
        self.grunt_sound.set_volume(MAX_VOLUME * 2)

        self.grunt_sound_played = False
    
    def import_key_graphics(self):
        self.key_animations = {'e':[]}

        main_path = f'./graphics/keys/'
        for animation in self.key_animations.keys():
            self.key_animations[animation] = import_folder(main_path + animation)

    def import_graphics(self):
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
            'down_idle':[], 'left_idle':[], 'up_idle':[], 'right_idle':[] }

        main_path = f'./graphics/oldman/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation, 'oldman')

    #show dialogue based on context of the level
    def show_dialogue(self, context):
        d = Dialogue()
        #if left, right, and top enemies are still remaining
        #beginning
        if context == 'lrt':
            d.show_dialogue("The fountain behind me used to be teeming with raw energy. But ever since this Ancient Meadow was taken over by evil forces, it hasn't been the same...", "Old Man")
        #defeated right side but not left
        elif context == 'lt':
            d.show_dialogue("I can feel the fountain responding to your actions! Whatever you're doing, you're doing it right! Keep it up.", "Old Man")
        #defeated left side but not right
        elif context == 'rt':
            d.show_dialogue("I can feel the fountain responding to your actions! Whatever you're doing, you're doing it right! Keep it up.", "Old Man")
        #just the final boss remaining (NEED TO WRAP TEXT)
        elif context == 't':
            d.show_dialogue("Amazing! The fountain can sense the runes you carry, but it needs more before it can be fully restored. You almost dispelled all the evil in the area. There should just be 1 more enemy.", "Old Man")
        #everything is defeated, start showing runes
        elif context == '':
            d.show_dialogue("You did it! You actually did it! Now go deposit your runes into the fountain. Be sure that you collected all of them, there should be 16 runes, each representing a single letter.", "Old Man")
            self.grunt_sound = pygame.mixer.Sound('./audio/oldman/miscellaneous_19_alex.wav')
            self.grunt_sound.set_volume(MAX_VOLUME * 2)
        if not self.grunt_sound_played:
            self.grunt_sound.play()
            self.grunt_sound_played = True


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

    def show_key(self, display_surface, pos):
        animation = self.key_animations['e']
        self.key_frame_index += self.key_animation_speed

        if self.key_frame_index >= len(animation):
            self.key_frame_index = 0
        
        self.key_image = animation[int(self.key_frame_index)]
        
        display_surface.blit(self.key_image, (pos[0] + 20, pos[1] - 10))
        self.grunt_sound_played = False

    def update(self):
        
        #self.move(self.speed)
        self.animate()
        if self.showing_dialogue:
            self.show_dialogue()



