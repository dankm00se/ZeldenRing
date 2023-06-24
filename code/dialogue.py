import pygame
from settings import *

class Dialogue:
    def __init__(self):
        
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #dialogue box setup
        self.dialogue_box_surface = pygame.Rect(80, self.display_surface.get_size()[1] / 3 * 2, self.display_surface.get_size()[0] - 160, self.display_surface.get_size()[1] / 3 - 20)
        self.max_char_count = 72

    def show_dialogue(self, text, character_name):


        character_surf = self.font.render(character_name, False, TEXT_COLOR) #maybe change to a different colour?
        character_x = 90
        character_y = self.display_surface.get_size()[1] / 3 * 2
        character_rect = character_surf.get_rect(topleft=(character_x, character_y))


        #draw everything
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.dialogue_box_surface)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.dialogue_box_surface, 3)

        #sort text into an array so that it can be displayed on multiple lines
        lines_of_text = self.sort_text_into_array(text)
        count = 1
        text_x = 100
        for line in lines_of_text:
            #spacing between lines of text
            text_y = self.display_surface.get_size()[1] / 3 * 2 + (30 * count)
            text_surf = self.font.render(line, False, TEXT_COLOR)
        
            text_rect = text_surf.get_rect(topleft=(text_x,text_y))
            self.display_surface.blit(text_surf, text_rect)
            count += 1
        #self.display_surface.blit(text_surf, text_rect)         
        self.display_surface.blit(character_surf, character_rect)

    def sort_text_into_array(self, text):
        length = len(text)
        lines_of_text = []
        last_letter = ''
        count = 0
        for x in range(self.max_char_count, length, self.max_char_count):
            
            last_letter = text[x] #get the last letter of the string, so we can append it to the next line

            #if the last char is NOT a space, then replace the character with a dash
            # and add the last letter to the beginning of the next line
            if not last_letter == ' ':
                text = text[:x - 1] + '-' + text[x - 1:]
                #text = text[:(x + 1)] + last_letter + text[(x + 1):]
            
            index = (self.max_char_count * count)
            lines_of_text.append(text[index:x])
            count += 1

        if length % self.max_char_count != 0:
            #get remaining characters of the string
            lines_of_text.append(text[length - length % self.max_char_count:])
        
        return lines_of_text

    def display(self):
        self.show_dialogue("hello world", "your mom")
        