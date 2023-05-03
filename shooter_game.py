#Создай собственный Шутер!
from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, image1, speed, x, y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(image1), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.speed
        if keys_pressed[K_RIGHT] and self.rect.x<627:
            self.rect.x+=self.speed
    def fire(self):
        bullet = Bullet("bullet.png", -15, ship.rect.centerx, ship.rect.top, 15,20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y >620:
            self.rect.y = 0
            self.rect.x = randint(0,615)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
lost = 0
last = 0
ship = Player("rocket.png", 8, 320, 390, 80, 100)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png",randint(1,4), randint(0,615), -40, 80, 50)
    monsters.add(monster)
bullets  = sprite.Group()

clock = time.Clock()
window = display.set_mode((700,500))
display.set_caption("Шутер")

background = transform.scale(image.load("galaxy.jpg"),(700,500))
mixer.init()
mixer.music.load("space.ogg")
fire_sound = mixer.Sound("fire.ogg")
game = True
finish = False

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE: #K_SPACE
                #fire_sound.play()
                ship.fire()
    if not(finish):
        window.blit(background, (0,0))
        monsters.update()
        bullets.update()
        ship.update() 
        test_lose = font1.render("Пропущено:" + str(lost), 1,(254, 255, 255))
        test_win = font1.render("Счёт:" + str(last), 1,(255, 255, 255))
        window.blit(test_win,(10, 20))
        window.blit(test_lose,(10, 50))
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
       #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            last += 1
            monster = Enemy("ufo.png" , randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)        

        if last >= 10:
            finish = True
            window.blit(win, (200, 200))

        if sprite.spritecollide(ship, monsters, False) or lost >= 3:
            finish = True
            window.blit(lose, (200, 200))
            mixer.music.stop()

    else:
        finish = False
        lose = 0
        lose =0 
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy("ufo.png",randint(1,4), randint(0,615), -40, 80, 50)
            monsters.add(monster)

    display.update()
    clock.tick(60)