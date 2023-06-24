from csv import reader
from os import walk
from natsort import natsorted
import pygame



def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter= ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path, type='none'):
    surface_list = []
    for _, __, img_files in walk(path):     
        for img in natsorted(img_files):
            full_path = path + '/' + img
            image_surf = pygame.image.load(full_path).convert_alpha()
            if(type == 'player'):
                image_surf = pygame.transform.scale(image_surf, (128, 128))
            if(type == 'bomb'):
                image_surf = pygame.transform.scale(image_surf, (32, 32))
            if(type == 'flame'):
                pass
            if(type == 'oldman'):
                image_surf = pygame.transform.scale(image_surf, (64, 64))
            if(type == 'biri'):
                image_surf = pygame.transform.scale(image_surf, (64, 64))
            if(type == 'health'):
                image_surf = pygame.transform.scale(image_surf, (64, 64))
            surface_list.append(image_surf)
    
    return surface_list

