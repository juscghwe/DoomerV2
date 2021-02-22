import math

class SETTINGS:
    ''' ALL STATIC VARIABLES '''
    '''Game'''
    FOLDER = ""
    FPS = 60
    SIZE = WIDTH, HEIGHT = (1024, 768)
    TITLE = "DOOMER"
    FULLSCREEN = True
    MOUSE_SENSITIVITY = 100

    '''Player'''
    PLAYER_START_HEALTH = 100
    PLAYER_START_ARMOR = 0
    PLAYER_MOVE_SPEED = 2
    PLAYER_ROT_SPEED = 3
    PLAYER_STRAF_SPEED = 1

    '''Shotgun'''
    SHOTGUN_START_AMO = 20
    SHOTGUN_MAX_AMO = 45
    SHOTGUN_LOAD = 2
    SHOTGUN_MAG = 2
    SHOTGUN_RELOADTIMER = 1
    SHOTGUN_MUZZLETIMER = 0.2
    SHOTGUN_IMG_FULL = "shotgun.png"
    SHOTGUN_IMG_EMPTY = "shotgunempty.png"
    SHOTGUN_IMG_SHOT = "shotgunfire.png"
    SHOTGUN_IMG_RELOAD = ["shotgunreload1.png", "shotgunreload2.png", "shotgunreload3.png"]
    SHOTGUN_MAX_DIST = 5
    SHOTGUN_MAX_RAD = 75
    # unused
    SHOTGUN_MAX_DAMAGE = 50 #pxls
    SHOTGUN_MAX_EFF_SURFACE = 50
    SHOTGUN_SHOT_CLUSTER = {"R":[[100, 1],[200, 0.5]],                  # R = Seitenabweichung, D = Abstand reversed von max damage;
                            "D":[[3, 1],[5, 0.5],[10, 0.2]]}            # Liste der Werte mit Liste (Abstand,Schaden); zwingend absteigend (vorn nach hinten, mitte nach außen)
                                                                                        
    '''Enemy'''
    ENEMY_START_HEALTH = 50
    ENEMY_DEATH_TIMER = 3
    ENEMY_SHOOT_TIME = 1
    ENEMY_COOLDOWN_TIME = 1

    '''Item'''
    HEALTH_PICKUP = 20
    ARMOR_PICKUP = 30
    SHOTGUN_PICKUP = 6

    '''MapItems'''
    MAPITEMS = {
        "wallred":1,
        "wallgreen":2,
        "wallblue":3,
        "wallwhite":4,
        "wallbloodeye":5,
        "wallbrick":6,
        "wallcolumn":7,
        "shotgunshell":94,
        "armour":95,
        "health":96,
        "enemy":97,
        "despawn":98,
        "spawn":99
        }

    '''Texture'''
    TEX_WIDTH = 64
    TEX_HEIGHT = 64