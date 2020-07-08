import math
import pygame
import random
from pygame import mixer

def hit (ojb1x, obj1y, obj2x, obj2y):  
    dist = math.sqrt(math.pow(ojb1x-obj2x, 2)+math.pow(obj1y-obj2y, 2))
    if dist < 34:
        return True
    else:        
        return False


def hit_pixel(object1, object2):
    
    offset = (int(object2.x - object1.x), int(object2.y - object1.y))
    point = object1.image_mask.overlap(object2.image_mask, offset)

    if point:
        return True
    return False

class EnemyWave():
    def __init__(self, count, spaceship):        
        self.enemy_list = []
        for i in range(count):
            self.enemy_list.append(Enemy(self.enemy_list, spaceship))

    def check(self, screen, bullet, spaceship, speed):
        score_tracker = 0
        for enemy in self.enemy_list:
            screen.blit(enemy.img, (int(enemy.x), int(enemy.y)))
            if enemy.x > 500 - enemy.img.get_rect().size[0] or enemy.x <= 0:
                enemy.velx *= -1  
            enemy.x += enemy.velx * speed
            enemy.y += enemy.vely * speed
            if enemy.y > 500:
                enemy.y = 0
                enemy.velx = enemy.velx * 1.5
            if bullet.shoot:
                if hit_pixel(bullet, enemy):
                    bullet.shoot = False
                    contact = mixer.Sound("sounds/explosion.wav")
                    contact.set_volume(.5)
                    # Killing the sound
                    #contact.play()
                    score_tracker += 1
                    enemy.new_location(self.enemy_list, spaceship)
                    enemy.speed_up()
                bullet.move(screen)

            if hit_pixel(enemy, spaceship):
                print(f'PLoss ---- \nSpaceship: {spaceship.x}, {spaceship.y} \nEnemy: {enemy.x},{enemy.y}')
                return -1

        return score_tracker


class Enemy():
    img_list = [pygame.image.load("images/ufo.png"), 
                pygame.image.load("images/ufo20.png"),
                pygame.image.load("images/ufo40.png"),
                pygame.image.load("images/ufo60.png"),
                pygame.image.load("images/ufo80.png"),
                pygame.image.load("images/ufo100.png")]
    
    def __init__(self, enemy_list, spaceship):
        self.velx = 15
        self.vely = 1
        self.img = Enemy.img_list[0]
        self.image_index = 0
        self.image_mask = pygame.mask.from_surface(self.img)
        self.new_location(enemy_list, spaceship)

    def new_location(self, enemy_list, spaceship):
        new_spot = True
        while new_spot:
            new_spot = False
            self.x = random.randint(self.img.get_rect().size[0], 500 - self.img.get_rect().size[0])
            self.y = random.randint(10, 250)
            for enemy in enemy_list:
                if self == enemy:
                    pass
                else:
                    #new_spot = hit(self.x, self.y, enemy.x, enemy.y)
                    if hit_pixel(self,enemy):
                        # If it hit something go back and start over
                        continue
            if hit_pixel(spaceship, self):
                continue
            else:
                break

    def speed_up(self):
        if abs(self.velx) > 30:
            self.vely *= 1.5
        else:
            self.velx *= 1.5
        if self.image_index < len(self.img_list) - 1:
            self.image_index += 1
            self.img = self.img_list[self.image_index]
            self.image_mask = pygame.mask.from_surface(self.img)
