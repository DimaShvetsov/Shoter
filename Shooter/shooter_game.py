#Создай собственный Shooter!
from pygame import *
from random import randint

from time import time as timer

win_width= 700
win_height= 500
display.set_caption('Shooter')
window= display.set_mode((win_width, win_height))
background = transform.scale(image.load('1644217642_31-abrakadabra-fun-p-pole-dlya-bravlov-44.png'),(win_width, win_height))


mixer.init()
mixer.music.load('Brawl Stars OST — - Battle 7 (vksaver) (www.lightaudio.ru).mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont(None, 80)
win = font1.render('Победа', True, (0, 255, 0))
lose = font1.render('Поражение', True, (200, 0, 0))
font2 = font.SysFont(None, 36)


score = 0 #Сбито
lost = 0 #Пропущено
max_lost = 3 #проиграли, если пропустили столько кораблей
goal = 10  #столько кораблей нужно сбить для победы
life = 3



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet=Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(30, win_width-30)
            self.rect.y = 0


class Ememy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1




class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



ship = Player('i.webp', 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 5):
    monster = Ememy('mytopkid.com-images-voron-30-800x800.jpg', randint(80, win_width - 80), - 40, 80, 50, randint(1, 5))
    monsters.add(monster)


asteroids = sprite.Group()

for i in range(1, 3):
    asteroid = Asteroids('8ceff65afb32fdc7ab5c35e91987a222.jpg', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()

run = True
finish = False


num_fire = 0
rel_time = False
while run:
    for e in event.get():


        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Счёт:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text2 = font2.render("Пропушено:" + str(lost), 1, (255, 255, 255))
        window.blit(text2, (10, 50))


        """движение спрайта"""
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        '''обновление местоположение спрайтов'''
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Подождите перезарядка...", 1, (200, 0 , 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time=False


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score+=1
            monster = Ememy('mytopkid.com-images-voron-30-800x800.jpg', randint(80, win_width - 80), - 40, 80, 50, randint(1, 5))
            monsters.add(monster)


        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1






            #Поражение
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

            #Победа
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if life == 3:
            life_color = (0, 200, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (200, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))


        display.update()
    time.delay(50)