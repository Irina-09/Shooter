from pygame import *
from random import *
clock = time.Clock()
W  = 700
H = 500
window = display.set_mode((W, H))
back = transform.scale(image.load("galaxy.jpg"), (W, H))
game = True
finish = False
lose = 0
check = 0
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(0.1)
fire = mixer.Sound("fire.ogg")
font.init()
font1 = font.Font(None, 36)
class GameSprite(sprite.Sprite):
    def __init__(self, image1, speed, x, y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(image1), (size_x,size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
 
class Enemy(GameSprite):
    def update(self):
        global lose
        self.rect.y += self.speed
        if self.rect.y >= 615:
            self.rect.y = 0
            lose += 1
            self.rect.x= randint(70, 620)

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", randint(1,3),randint(70, 620), -40, 80, 50 )
    monsters.add(enemy)
class Player(GameSprite):
    def updateSprites(self):
        keys_pressed = key.get_pressed() 

        if keys_pressed[K_LEFT] and self.rect.x > 5: 
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT]and self.rect.x < 620 : 
            self.rect.x += self.speed 
    def fire(self):
        bullet = Bullet("bullet.png",-15, self.rect.centerx, self.rect.top, 15, 20 )
        bullets.add(bullet)
rocket = Player("rocket.png", 8, 320, 390, 65, 100)
font2 =  font.Font(None, 70)
win1 = font2.render("ПОБЕДА!", 1, (255, 255, 255))
lose1 = font2.render("Ты проиграл", 1, (180, 0, 0))
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                fire.play()
                fire.set_volume(0.1)


    if not(finish):
        window.blit(back, (0,0))
        rocket.updateSprites()
        rocket.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        
        collide = sprite.groupcollide(monsters, bullets, True, True)
        for c in collide:
            check  += 1
            enemy = Enemy("ufo.png", randint(1,3),randint(70, 620), -40, 80, 50 )
            monsters.add(enemy)
        lose_txt = font1.render("Пропущено " + str(lose), 1, (255, 255, 255))
        win = font1.render("Счет " + str(check), 1, (255, 255, 255))
        window.blit(win, (10, 20))
        window.blit(lose_txt, (10, 40))
        if check >= 10:
            finish = True
            window.blit( win1, (200, 200))
            mixer.music.stop()

        if sprite.spritecollide(rocket, monsters, False) or lose >= 3:
            finish = True
            window.blit( lose1, (200, 200))
            mixer.music.stop()

    else:
        finish = False
        check = 0
        lose = 0 
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
  
        for i in range(5):
            enemy = Enemy("ufo.png", randint(1,3),randint(70, 620), -40, 80, 50 )
            monsters.add(enemy)
        mixer.music.play()
        mixer.music.set_volume(0.1)

    display.update()
    clock.tick(60)
