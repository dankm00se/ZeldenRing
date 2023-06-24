import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        
        #general setup        
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Zelden Ring')
        self.clock = pygame.time.Clock()
        
        self.level = Level()
        #sound
        self.main_sound = pygame.mixer.Sound('./audio/ambience/main.wav')
        self.main_sound.set_volume(MAX_VOLUME * 5) 
        self.main_sound.play(loops = -1)

        self.boss_sound = pygame.mixer.Sound('./audio/ambience/boss.wav')
        self.boss_sound.set_volume(MAX_VOLUME * 5)        
        #print(main_sound.get_volume())
        self.music_changed = False
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        #self.level.toggle_menu()
                        pass
                    if event.key == pygame.K_p:
                        #self.level.play_video()
                        pass
                
            
            self.screen.fill(WATER_COLOR) 
            self.level.run()

            if self.level.spawn_top and not self.music_changed:
                self.main_sound.stop()
                self.boss_sound.play()
                self.music_changed = True
            if self.level.player.runes == 16:
                self.main_sound.play(loops= -1)
            
            if self.level.player.health <= 0:
                self.main_sound.stop()
                self.boss_sound.stop()
                
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()