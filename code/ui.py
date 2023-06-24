import pygame
from settings import *

class UI:
    def __init__(self):
        
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.game_over_fade = 0
        self.image = pygame.image.load('./graphics/gameover/gameover.jpg').convert_alpha()

        #bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        #convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        self.potion_graphic = pygame.image.load('./graphics/items/BigHealthPotionMoving1.png').convert_alpha()
        self.potion_graphic = pygame.transform.scale(self.potion_graphic, (64, 64))
        #convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        #draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        #converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20), 3)

    def show_runes(self, num_runes):
        text_surf = self.font.render(str(int(num_runes)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[0] - 20
        text_rect = text_surf.get_rect(bottomright=(x,y))

           
        #title text
        title_surf = self.font.render("Runes x " + str(num_runes), False, TEXT_COLOR)
        title_rect = title_surf.get_rect(midtop = pygame.math.Vector2(80, 60))

      
        #draw everything
        self.display_surface.blit(title_surf, title_rect)
        

    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect


    def potion_overlay(self, num_potions):
        bg_rect = self.selection_box(10, 630)
        potion_surf = self.potion_graphic
        potion_rect = potion_surf.get_rect(center = bg_rect.center)

        text_surf = self.font.render(" x " + str(num_potions), False, TEXT_COLOR)
        #LEFT OFF HERE, NEED TO ADJUST POTIONS NUMBER

        self.display_surface.blit(potion_surf, potion_rect)
        self.display_surface.blit(text_surf, potion_rect)


    def show_game_over(self):
        game_over_surface = pygame.Surface((WIDTH, HEIGHT))
        game_over_surface.set_alpha(self.game_over_fade)
        self.image.set_alpha(-255 + self.game_over_fade)    

        bg_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        image_rect = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 60, 438, 133)

        pygame.draw.rect(game_over_surface, pygame.Color(0, 0, 0), bg_rect)

        self.game_over_fade += 2        

        self.display_surface.blit(game_over_surface, bg_rect)
        self.display_surface.blit(self.image, image_rect)

        if self.game_over_fade > 1000:
            return True
        else:
            return False


    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.potion_overlay(player.potions)
        self.show_runes(player.runes)
   
       

        
        