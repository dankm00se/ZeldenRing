#game setup
WIDTH       = 1280
HEIGHT      = 720
FPS         = 60
TILESIZE    = 32
HITBOX_OFFSET = {
    'player': -100,
    'wall': -20,
    'grass': -10,
    'invisible': 0,
    'pillar': -40,
    'trigger': 0,
    'breakable': -20
}

#ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = './graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'
 

#general colours
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

#ui colours
HEALTH_COLOR= 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

#weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'./graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30,'graphic':'./graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic':'./graphics/weapons/axe/full.png'},
    'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'./graphics/weapons/rapier/full.png'},
    'sai':{'cooldown': 80, 'damage': 10, 'graphic':'./graphics/weapons/sai/full.png'},

    }
 
#magic
magic_data = {
    'flame' : {'strength': 5, 'cost' : 20, 'graphic':'./graphics/particles/flame/fire.png', 'cooldown' : 200},
    'heal' : {'strength' : 20, 'cost' : 10, 'graphic': './graphics/particles/heal/heal.png', 'cooldown' : 200}
}

#enemy
monster_data = {
    'squid': {'health': 1,'exp':100,'damage':30,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 40, 'notice_radius': 360},
    'raccoon': {'health': 3,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'./audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 1,'exp':110,'damage':20,'attack_type': 'thunder', 'attack_sound':'./audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 7,'exp':120,'damage':20,'attack_type': 'leaf_attack', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 40, 'notice_radius': 300},
    'darklink': {'health': 70,'exp':120,'damage':10,'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 40, 'notice_radius': 300, 'bomb_radius': 100},
    'ganon': {'health': 500, 'exp': 1000, 'damage':20, 'attack_type': 'slash', 'attack_sound':'./audio/attack/slash.wav', 'speed': 1, 'resistance': 10, 'attack_radius': 80, 'notice_radius': 400, 'fire_radius':200},
    'biri': {'health': 25, 'exp': 0, 'damage': 30, 'attack_type': 'leaf_attack', 'attack_sound':'./audio/attack/slash.wav', 'speed': 2, 'resistance': 10, 'attack_radius': 40, 'notice_radius': 350}}

#volume
MAX_VOLUME = 0.05