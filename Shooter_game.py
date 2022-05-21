from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 170)
lose = font2.render("YOU LOSE!", True, (180,0,0))
win = font2.render("YOU WIN!", True, (255,255,255))

mixer.init()
mixer.music.load("Odyssey.ogg")
mixer.music.play()
fire_sound = mixer.Sound("arti.ogg")

mw = display.set_mode((900,700))
display.set_caption("Space shooter")
mw_width = 900
mw_height = 700
bg = transform.scale(image.load("milkyway.jpg"),(mw_width,mw_height))

img_hero = image.load("spaceX.png")
img_enemy = image.load("NLO.png")
img_rocket = image.load("rocket.png")
img_asteroid = image.load("enemy.png")

lost = 0
score = 0
max_lost = 10
goal = 20
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(player_image, (size_x,size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < mw_width - 100:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_rocket, self.rect.centerx, 
                self.rect.top, 20,60, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > mw_height:
            self.rect.y = 0
            self.rect.x = randint(0, mw_width-50)
            lost += 1

class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #global lost
        if self.rect.y > mw_height:
            self.rect.y = 0
            self.rect.x = randint(0, mw_width-50)
        #    lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player(img_hero, 450, 600, 80, 100, 10)
monsters = sprite.Group()
for i in range(1,7):
    monster = Enemy(img_enemy, randint(0, mw_width-50), -50, 90, 60, randint(1,4))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1,4):
    asteroid = Enemy2(img_asteroid, randint(0, mw_width-50), -40, 50, 50, randint(2,6))
    asteroids.add(asteroid)

game = True
finish = False
rel_time = False
num_fire = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        mw.blit(bg,(0,0))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(mw)
        asteroids.draw(mw)
        bullets.draw(mw)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render("Ждите, перезарядка...", 1, (240, 240, 240))
                mw.blit(reload, (370, 660))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(0, mw_width-50), -50, 90, 60, randint(1,4))
            monsters.add(monster)
    
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            mw.blit(lose, (200,200))

        if score >= goal:
            finish = True
            mw.blit(win, (200,200))

        text = font1.render("Счет: " + str(score), 1, (255,255,255))
        mw.blit(text,(10,20))
        text2 = font1.render("Пропущено: " + str(lost), 1, (255,255,255))
        mw.blit(text2, (10,50))        

        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)

        text_life = font1.render("Количество жизни: " + str(life), 1, life_color)
        mw.blit(text_life, (640,10))
        
        display.update()
    
   #clock.tick(FPS)
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for n in asteroids:
            n.kill()
    
        time.delay(3000)
    
        for i in range(1,7):
            monster = Enemy(img_enemy, randint(0, mw_width-50), -50, 90, 60, randint(1,4))
            monsters.add(monster)
        for i in range(1,4):
            asteroid = Enemy(img_asteroid, randint(0, mw_width-50), -40, 50, 50, randint(2,6))
            asteroids.add(asteroid)

    time.delay(40)
######
    


