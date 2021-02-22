import pygame
import math
import script.general.loader as ld
from SETTINGS import SETTINGS

class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.__WIDTH, self.__HEIGHT = pygame.display.get_surface().get_size()

        self.name = "shotgun"
        filepath = SETTINGS.FOLDER
        self.__fire_img = ld.loadimage(filepath, "images/gameobjects", "shotgunfire.png")
        self.weapon_img = ld.loadimage(filepath, "images/gameobjects", "shotgun.png")
        self.__weapon_empty_img = ld.loadimage(filepath, "images/gameobjects","shotgunempty.png")
        self.__weapon_reload_img1 = ld.loadimage(filepath, "images/gameobjects","shotgunreload1.png")
        self.__weapon_reload_img2 = ld.loadimage(filepath, "images/gameobjects","shotgunreload2.png")
        self.__weapon_reload_img3 = ld.loadimage(filepath, "images/gameobjects","shotgunreload3.png")
        self.img = self.weapon_img

        weapon_WIDTH, weapon_HEIGHT = self.weapon_img.get_size()
        fire_WIDTH, fire_HEIGHT = self.__fire_img.get_size()
        self.__weapon_pos = (self.__WIDTH / 2 - weapon_WIDTH / 2, self.__HEIGHT - weapon_HEIGHT)
        self.__fire_pos = (self.__WIDTH / 2 - fire_WIDTH / 2, self.__HEIGHT - weapon_HEIGHT - fire_HEIGHT / 2)
        
        self.max_amo = SETTINGS.SHOTGUN_MAX_AMO
        self.load = SETTINGS.SHOTGUN_LOAD
        self.mag = SETTINGS.SHOTGUN_MAG
        self.amo = SETTINGS.SHOTGUN_START_AMO
        self.amo_pickup = SETTINGS.SHOTGUN_PICKUP
        self.__max_dist = SETTINGS.SHOTGUN_MAX_DIST
        self.__max_rad = SETTINGS.SHOTGUN_MAX_RAD
        #self.__max_eff = SETTINGS.SHOTGUN_MAX_EFF_SURFACE
        #self.__cluster_dist = SETTINGS.SHOTGUN_SHOT_CLUSTER["D"]
        #self.__cluster_rad = SETTINGS.SHOTGUN_SHOT_CLUSTER["R"]
        #self.__dist_scale = self.__cluster_dist[0][0]
        self.__reloading = False
        self.__reloadcounter = 0
        self.__reloadtime = SETTINGS.SHOTGUN_RELOADTIMER * SETTINGS.FPS
        self.__muzzle = False
        self.__muzzlecounter = 0
        self.__muzzletime = int(SETTINGS.SHOTGUN_MUZZLETIMER * SETTINGS.FPS)
        self.__empty = False

    def shoot(self, target_surface, player_pos, enemy_group):
        ''' Adjusts load and calls shootray. Shoots only when not reloading. '''
        if self.load <= 0 and self.__reloading == False and self.amo > 0 and self.__empty == False:
            self.__reloading = True
        elif self.load <= 0 and self.amo == 0:
            self.__empty = True
            self.img = self.__weapon_empty_img
        elif self.__reloading == False and self.__empty == False:
            enemy_group = self.__shoot_ray(player_pos, enemy_group)
            self.__muzzle = True
            self.load -= 1
        return enemy_group

    def __shoot_ray(self, player_pos, enemy_group):
        for enemy in sorted(enemy_group, key=lambda spr: spr.dist):
            dist = math.sqrt(enemy.dist)
            rad = abs(self.__WIDTH / 2 - enemy.center)
            if dist < self.__max_dist and rad < self.__max_rad and enemy.visible:
                enemy.health -= 50
            #dist = math.sqrt(enemy.dist)
            #rad = abs(self.__WIDTH / 2 - enemy.center) / (self.__max_dist - dist) * self.__dist_scale
            #print(dist, rad)
            #if dist < self.__max_dist and enemy.visible:
            #    for i in range(len(self.__cluster_dist)):
            #        if dist < self.__cluster_dist[i][0]:
            #            dist_factor = self.__cluster_dist[i][1]
            #    for i in range(len(self.__cluster_rad)):
            #        if rad < self.__cluster_rad[i][0]:
            #            rad_factor = self.__cluster_rad[i][1]
            #    surf_factor = min(enemy.width * self.__max_eff / enemy.sprite_width, self.__max_eff)
            #    try:
            #        damage = dist_factor * rad_factor * surf_factor
            #        print(f"Damage: {damage} = {dist_factor} * {rad_factor} * {surf_factor}")
            #    except NameError:
            #        damage = 0
            #    enemy.health -= damage
        # Durchschüsse vermeiden oder damage anpassen
        return enemy_group

    def update(self,target_surface,true_fps):
        if self.__muzzle == True:
            self.__muzzleanimation(target_surface, true_fps)
        if self.__reloading == True:
            self.__reloadanimation(true_fps)        
        target_surface.blit(self.img, self.__weapon_pos)

    def __reload(self):
        ''' mathmatical reloading '''
        self.__reloading = False
        if self.amo >= self.mag:
            self.amo -= self.mag - self.load
            self.load = self.mag
        elif self.amo < self.mag:
            self.load = self.amo
            self.amo = 0
        self.img = self.weapon_img

    def __muzzleanimation(self, target_surface, true_fps):
        ''' muzzleflash animation '''
        if true_fps == 0: true_fps = SETTINGS.FPS
        self.__muzzletime = int(SETTINGS.SHOTGUN_MUZZLETIMER * true_fps)
        if self.__muzzlecounter <= self.__muzzletime:
            self.__muzzlecounter +=1
            target_surface.blit(self.__fire_img, self.__fire_pos)
        else:
            self.__muzzle = False
            self.__muzzlecounter = 0

    def __reloadanimation(self, true_fps):
        ''' reload animation, reloads at its end '''
        if true_fps == 0: true_fps = SETTINGS.FPS
        self.__reloadtime = int(SETTINGS.SHOTGUN_RELOADTIMER * true_fps)
        if self.__reloadcounter <= self.__reloadtime:
            self.__reloadcounter += 1 
            if self.__reloadcounter <= self.__reloadtime / 3:
                self.img = self.__weapon_reload_img1
            elif self.__reloadtime / 3 < self.__reloadcounter <= 2 * self.__reloadtime / 3:
                self.img = self.__weapon_reload_img2
            else:
                self.img = self.__weapon_reload_img3
        else:
            self.__reload()
            self.__reloadcounter = 0