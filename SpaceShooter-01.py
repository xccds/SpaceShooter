
import pygame
import sys
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self,resources,all_sprites,bullets):
        super().__init__()
        self.resources = resources
        self.bullets = bullets
        self.image = pygame.transform.scale(resources.player_img, (50, 38))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.all_sprites = all_sprites
        self.all_sprites.add(self)


    def update(self):

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
        if keystate[pygame.K_SPACE] :
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, resources):
        super().__init__()
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

class Resources:
        
        def __init__(self):

            # image load
            self.player_img = pygame.image.load(path.join(img_dir, "playerShip3_red.png")).convert_alpha()
            self.bullet_img = pygame.image.load(path.join(img_dir, "laserRed05.png")).convert_alpha()

            # Load all game sounds
            self.shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Shot.wav'))
            self.shoot_sound.set_volume(0.2)
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
        self.running = True
        self.setup_sprite()

    def setup_sprite(self):
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(self.resources, self.all_sprites, self.bullets)


    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def play(self):
        # Game loop

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
 
            # Draw / render
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.play()