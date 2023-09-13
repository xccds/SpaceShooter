
import pygame
import random
import sys
import math
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
PI = 3.1415

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

    

class Player(pygame.sprite.Sprite):
    def __init__(self,resources,all_sprites,bullets):
        pygame.sprite.Sprite.__init__(self)
        self.resources = resources
        self.bullets = bullets
        self.image = pygame.transform.scale(resources.player_img, (50, 38))
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.all_sprites = all_sprites
        self.all_sprites.add(self)


    def update(self):

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.rect.left>0:
            self.speedx = -6
        if keystate[pygame.K_RIGHT] and self.rect.right<WIDTH:
            self.speedx = 6
        if keystate[pygame.K_UP] and self.rect.top>0:
            self.speedy = -6
        if keystate[pygame.K_DOWN] and self.rect.bottom<HEIGHT:
            self.speedy = 6
        if keystate[pygame.K_SPACE] and not self.hidden:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top,self.resources)
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)
            self.resources.shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, resources):
        pygame.sprite.Sprite.__init__(self)
        self.image = resources.bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, resources, all_sprites, mobs):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(resources.meteor_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        all_sprites.add(self)
        mobs.add(self)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, index, degree, direction, resources, all_sprites, enemy_group, enemy_bullets):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(resources.enemy_img, (50, 38))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.degree = PI * degree / 180
        self.speed = 4
        self.direction = direction
        self.shoot_delay = 550
        self.last_shot = pygame.time.get_ticks()
        self.resources = resources
        self.all_sprites = all_sprites
        self.enemy_bullets = enemy_bullets

        if direction == "right":
            self.rect.centerx = -10 - index * 80 *  math.cos(self.degree)
            self.rect.centery = -10 - index * 80 *  math.sin(self.degree)
            self.speedx = self.speed * math.cos(self.degree)
            self.speedy = self.speed * math.sin(self.degree)
        if direction == "left":
            self.rect.centerx = WIDTH+10 + index * 80 *  math.cos(self.degree)
            self.rect.centery = -10 - index * 80 *  math.sin(self.degree)
            self.speedx = - self.speed * math.cos(self.degree)
            self.speedy = self.speed * math.sin(self.degree)

        all_sprites.add(self)
        enemy_group.add(self)

    def update(self):
        
        self.rect.x += self.speedx 
        self.rect.y += self.speedy
        if self.direction == "left" and (self.rect.top > HEIGHT + 50 or self.rect.right < -50):
            self.kill()
        if self.direction == "right" and (self.rect.top > HEIGHT + 50 or self.rect.left > WIDTH+50):
            self.kill()
        if random.random() > 0.8:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom,self.resources)
            self.all_sprites.add(bullet)
            self.enemy_bullets.add(bullet)
            self.resources.shoot_sound.play()  
            self.all_sprites.add(self)
            self.enemy_bullets.add(self)      

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, resources):
        pygame.sprite.Sprite.__init__(self)
        self.image = resources.enemy_bullet_img
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 8

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()


class Resources:
        
        def __init__(self):

            # image load
 
            self.player_img = pygame.image.load(path.join(img_dir, "playerShip3_red.png")).convert_alpha()
            self.player_mini_img = pygame.transform.scale(self.player_img, (25, 19))
            self.bullet_img = pygame.image.load(path.join(img_dir, "laserRed05.png")).convert_alpha()
            self.enemy_bullet_img = pygame.image.load(path.join(img_dir, "laserBlue05.png")).convert_alpha()
            self.enemy_img = pygame.image.load(path.join(img_dir, "enemyBlue1.png")).convert_alpha()


            self.meteor_images = []
            meteor_list = ['meteorBrown_med1.png',
                        'meteorGrey_med2.png', 'meteorBrown_small1.png', 'meteorGrey_small2.png',
                        'meteorBrown_tiny1.png','meteorGrey_tiny2.png']
            for img in meteor_list:
                self.meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert_alpha())


            # Load all game sounds
            self.shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Shot.wav'))
            self.shoot_sound.set_volume(0.2)
            self.enemy_shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'sfx_laser1.ogg'))
            self.enemy_shoot_sound.set_volume(0.1)
            self.mob_expl_sound = pygame.mixer.Sound(path.join(snd_dir, 'expl6.wav'))
            self.mob_expl_sound.set_volume(0.4)
            self.enemy_expl_sound = pygame.mixer.Sound(path.join(snd_dir, 'Explosion.wav'))
            self.enemy_expl_sound.set_volume(0.4)
            self.player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
            pygame.mixer.music.load(path.join(snd_dir, 'action.wav'))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(loops=-1)

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("space shooter")
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font('arial')
        self.resources = Resources()
        self.game_over = True
        self.running = True
        self.score = 0
        self.setup_sprite()

    def setup_sprite(self):
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player = Player(self.resources, self.all_sprites, self.bullets)


    def be_damaged(self):
        if self.player.shield <= 0:
            self.resources.player_die_sound.play()
            self.player.hide()
            self.player.lives -= 1
            self.player.shield = 100
    
    def bullet_hit_mob(self):
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in hits:
            self.score += 50 - hit.radius
            self.resources.mob_expl_sound.play()
            Mob(self.resources, self.all_sprites, self.mobs)

    def bullet_hit_enemy(self):
        hits = pygame.sprite.groupcollide(self.enemy_group, self.bullets, True, True)
        for hit in hits:
            self.score += 50 
            self.resources.enemy_expl_sound.play()

    def bullet_hit_player(self):
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= 30
            self.resources.enemy_expl_sound.play()
            self.be_damaged()

    def enemy_hit_player(self):
        hits = pygame.sprite.spritecollide(self.player, self.enemy_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= 50
            self.resources.enemy_expl_sound.play()
            self.be_damaged()

    def mob_hit_player(self):
        hits = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= hit.radius * 2
            self.resources.enemy_expl_sound.play()
            Mob(self.resources, self.all_sprites, self.mobs)
            self.be_damaged()


    def new_mob(self,size=6):
        for _ in range(size):
            Mob(self.resources, self.all_sprites, self.mobs)  

    def new_enemy_group(self, size=4):
        direction = random.choice(["left","right"])
        degree = random.randrange(20,70)
        for i in range(size):
            Enemy(i, degree,direction, self.resources, self.all_sprites, self.enemy_group, self.enemy_bullets)
            
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def play(self):
        # Game loop
        self.new_mob()
        self.new_enemy_group()
        while self.running:

            # keep loop running at the right speed
            self.clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.running = False
            # Update
            self.all_sprites.update()
            self.bullet_hit_mob()
            self.mob_hit_player()
            self.bullet_hit_enemy()
            self.bullet_hit_player()
            self.enemy_hit_player()

            if len(self.enemy_group)==0:
                self.new_enemy_group()
            # if the player died and the explosion has finished playing
            if self.player.lives == 0:
                self.running = False
            # Draw / render
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.play()