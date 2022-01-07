import pygame
from pygame.locals import *
import random
from scripts import button
import shelve
import sys
import os

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("A game about real men")
icon = pygame.image.load('data/images/icon.png')
pygame.display.set_icon(icon)

#set Fraemrate
clock = pygame.time.Clock()
FPS = 60

#load images
logo_menu = pygame.image.load('data/images/UI/Logo menu.png')
start_img = pygame.image.load('data/images/UI/start_btn.png').convert_alpha()
play_img = pygame.image.load('data/images/UI/play_btn.png').convert_alpha()
load_img = pygame.image.load('data/images/UI/load_btn.png').convert_alpha()
exit_img = pygame.image.load('data/images/UI/exit_btn.png').convert_alpha()
walkLeft = [pygame.image.load('data/images/Player/L1.png')]
walkRight = [pygame.image.load('data/images/Player/R1.png')]
char = pygame.image.load('data/images/Player/standing.png')
bg0 = pygame.image.load('data/images/Backgrounds/720p/bg0.png')
bg1 = pygame.image.load('data/images/Backgrounds/720p/bg1.png')
bg2 = pygame.image.load('data/images/Backgrounds/720p/bg2.png')
bg3 = pygame.image.load('data/images/Backgrounds/720p/bg3.png')
bg4 = pygame.image.load('data/images/Backgrounds/720p/bg4.png')
bg5 = pygame.image.load('data/images/Backgrounds/720p/bg5.png')

#load sounds
deathSound = pygame.mixer.Sound('data/sounds/alkash_died.mp3')
coughSounds = [pygame.mixer.Sound('data/sounds/cough1.mp3'), pygame.mixer.Sound('data/sounds/cough2.mp3'), pygame.mixer.Sound('data/Sounds/cough3.mp3'), pygame.mixer.Sound('data/sounds/cough4.mp3')]
hitSounds = [pygame.mixer.Sound('data/sounds/hit1.mp3'), pygame.mixer.Sound('data/sounds/hit2.mp3')]
slurpSounds = pygame.mixer.Sound('data/sounds/Хрум.mp3')
eatSounds = [pygame.mixer.Sound('data/sounds/А вкуснотища та какая.mp3'), pygame.mixer.Sound('data/sounds/Вкусно как.mp3')]
fightSounds = [pygame.mixer.Sound('data/sounds/Cерпом и молотом по яйцам!.wav'), pygame.mixer.Sound('data/sounds/Cерпом и молотом по яйцам!.wav')]
phoneCallSound = pygame.mixer.Sound('data/sounds/phone call.mp3')

#load music
soundtracks = ['data/sounds/soundtracks/M.O.O.N. - Crystals.mp3', 'data/sounds/soundtracks/Sun Araw - Horse Steppin.mp3', 'data/sounds/soundtracks/Scattle - Knock Knock.mp3', 'data/sounds/soundtracks/Perturbator - ElectricDreams.mp3','data/sounds/silence.mp3']
pygame.mixer.music.load('data/sounds/soundtracks/Untitled.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

#define colours
RED = (255, 0, 0)
WHITE = (255, 255, 255)
VIOLET = (155, 0, 182)
BLACK = (0, 0, 0)
col_spd = 1
col_dir = [-1, 1, -1]
def_col = [120, 120, 240]
orig_surf = bg1
alpha = 255  
orig_surf2 = bg0
alpha2 = 0

#define game variables
d = shelve.open('data/data')
GRAVITY = 0.25
x_limitation = 400
y_limitation = [[177, 128], [200, 128], [177, 128], [320, 260], [350, 128]]
screen_scroll = 0
final_level = 5
current_level = 1
backgrounds = [bg1, bg2, bg3, bg4, bg5]
bgX0 = backgrounds[current_level-1].get_width()*-1
bgX1 = 0
bgX2 = backgrounds[current_level-1].get_width()
time = 0
score = 0

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def draw_bg():
    global bgX0
    global bgX1
    global bgX2
    
    screen.blit(backgrounds[current_level-1], (bgX0, 0))  # рисует нуливое изображение bg
    screen.blit(backgrounds[current_level-1], (bgX1, 0))  # рисует первое изображение bg
    screen.blit(backgrounds[current_level-1], (bgX2, 0))  #рисует второе изображение bg
    
    if bgX0 > backgrounds[current_level-1].get_width():
        bgX0 = backgrounds[current_level-1].get_width() * -1

    if bgX1 > backgrounds[current_level-1].get_width():
        bgX1 = backgrounds[current_level-1].get_width() * -1

    if bgX2 > backgrounds[current_level-1].get_width():
        bgX2 = backgrounds[current_level-1].get_width() * -1

    if bgX0 < backgrounds[current_level-1].get_width() * -1:  
        bgX0 = backgrounds[current_level-1].get_width()

    if bgX1 < backgrounds[current_level-1].get_width() * -1:  
        bgX1 = backgrounds[current_level-1].get_width()
    
    if bgX2 < backgrounds[current_level-1].get_width() * -1:
        bgX2 = backgrounds[current_level-1].get_width()
        
bonus_level = 0       
def get_liminal_screen(img1, img2, fade_time):
    global alpha
    global alpha2
    global bgX0
    global bgX1
    global bgX2
    global bg0
    global backgrounds
    global time
    global fade
    global score
    global bonus_level

    if time == 0:
        bonus_level = score
        fade = True
    
    if fade:
        time += 1
        if alpha > 0:
            alpha -= 13
            alpha = max(0, alpha)  # Make sure it doesn't go below 0.
            img1 = change_alpha(orig_surf, alpha)
        if alpha2 < 255:
            alpha2 += 13
            alpha2 = min(255, alpha2)
            img2 = change_alpha(orig_surf2, alpha2)
            
    if time >= fade_time:
        fade = False
        if alpha2 > 0:
            alpha2 -= 13
            alpha2 = max(0, alpha2)
            img2 = change_alpha(orig_surf2, alpha2)
      
        if alpha < 255:
            alpha += 13
            if bonus_level == 13:
                alpha = min(255, alpha)
            else:
                alpha = max(255, alpha)
            img1 = change_alpha(orig_surf, alpha)

        if alpha == 255 and alpha2 == 0:
            time = 0
        
    screen.blit(img2, (bgX0, 0))
    screen.blit(img2, (bgX1, 0))
    screen.blit(img2, (bgX2, 0))
    

def change_alpha(orig_surf, alpha):
    surf = orig_surf.copy()
    alpha_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    alpha_surf.fill((255, 255, 255, alpha)) 
    surf.blit(alpha_surf, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
    return surf


def draw_text(text, size, col, x, y):
    font = 'data/Hotlien Odessa.otf'
    font = pygame.font.Font(font, size)
    text_surfase = font.render(text, True, col)
    text_rect = text_surfase.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surfase,text_rect)


def col_change(col, dir):
    for i in range (3):
        col[i] += col_spd * dir[i]
        if col[i] >= 255 or col[i] <= 0:
            dir[i] *= -1


class player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.damage = 1 - (current_level//8)
        self.vel = 5 - (current_level//4)
        self.collisions = False
        self.isJump = False
        self.left = False
        self.right = True
        self.standing = False
        self.walkCount = 0
        self.jumpCount = 8
        self.hitbox = (self.x, self.y, 62, 120)

    def draw(self, screen):
        if self.walkCount + 1 >= 1:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                screen.blit(walkLeft[self.walkCount//1], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//1], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x, self.y, 62, 120)
       # pygame.draw.rect(screen, (255,0,0), self.hitbox,2)

    def hit(self):
        self.score -= 0

class enemy(object):
    def __init__(self, x, y, area_move, health, damage, vel):
        self.x = x
        self.y = y
        self.area_move = area_move
        self.health = health
        self.max_health = self.health
        self.damage = damage 
        self.vel = vel
        self.max_vel = (self.vel - 2) * current_level
        self.min_vel = (self.vel + 2) * current_level
        self.hitbox = (self.x, self.y, 31, 57)
        self.visible = True

        
class cat(enemy):
    skin_1_Walk = [pygame.image.load('data/images/Enemys/Cats/Cat 1/L1.png'), pygame.image.load('data/images/Enemys/Cats/Cat 1/L2.png'), pygame.image.load('data/images/Enemys/Cats/Cat 1/L3.png'), pygame.image.load('data/images/Enemys/Cats/Cat 1/L4.png'), pygame.image.load('data/images/Enemys/Cats/Cat 1/L5.png'), pygame.image.load('data/images/Enemys/Cats/Cat 1/L6.png')]
    skin_1_Death = [pygame.image.load('data/images/Enemys/Cats/Cat 1/Death1.png'),pygame.image.load('data/images/Enemys/Cats/Cat 1/Death2.png'),pygame.image.load('data/images/Enemys/Cats/Cat 1/Death3.png'),pygame.image.load('data/images/Enemys/Cats/Cat 1/Death4.png')]
    skin_1 = [skin_1_Walk, skin_1_Death]
    
    skin_2_Walk = [pygame.image.load('data/images/Enemys/Cats/Cat 2/L1.png'), pygame.image.load('data/images/Enemys/Cats/Cat 2/L2.png'), pygame.image.load('data/images/Enemys/Cats/Cat 2/L3.png'), pygame.image.load('data/images/Enemys/Cats/Cat 2/L4.png'), pygame.image.load('data/images/Enemys/Cats/Cat 2/L5.png'), pygame.image.load('data/images/Enemys/Cats/Cat 2/L6.png')]
    skin_2_Death = [pygame.image.load('data/images/Enemys/Cats/Cat 2/Death1.png'),pygame.image.load('data/images/Enemys/Cats/Cat 2/Death2.png'),pygame.image.load('data/images/Enemys/Cats/Cat 2/Death3.png'),pygame.image.load('data/images/Enemys/Cats/Cat 2/Death4.png')]
    skin_2 = [skin_2_Walk, skin_2_Death]
    
    skins = [skin_1, skin_2]
    current_skin = skins[random.randint(0, len(skins)-1)]
    walk_Animation = current_skin[0]
    death_Animation = current_skin[1]
    walkCount = 0
    deathCount = 0
    death = False
    
    def __init__(self):                                         
         super().__init__(x = SCREEN_WIDTH, y = 0, area_move = [75, 135], health = 1, damage = 0, vel = 7)

       
    def draw(self, screen):
        if self.visible:
            if not (self.death):
                self.move()
                if self.walkCount + 1 >= 12:
                    self.walkCount = 0
           
                screen.blit(self.walk_Animation[self.walkCount //2], (self.x, self.y))
                self.walkCount += 1
            else:
                if self.deathCount < 8:
                    screen.blit(self.death_Animation[self.deathCount //2], (self.x, self.y))
                    self.deathCount += 2
                else: 
                    self.deathh()
                    self.deathCount = 0
            
            self.hitbox = (self.x, self.y, 38, 19)
            #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)


    def move(self):
       if self.x > -30:
            self.x -= self.vel
            
            
    def deathh(self):
        global score       
        score += 2
        self.health = 0
        slurpSounds.play()
        eatSounds[random.randint(0, len(eatSounds)-1)].play()
        
        
    def hit(self):
        hitSounds[random.randint(0, len(hitSounds)-1)].play()
        if self.health > man.damage:
            self.health -= man.damage
        else:
            self.death = True


    def update(self):
        self.death = False
        self.health = self.max_health
        self.current_skin = self.skins[random.randint(0, len(self.skins)-1)]
        self.walk_Animation = self.current_skin[0]
        self.death_Animation = self.current_skin[1]
        self.x = SCREEN_WIDTH
        self.y = random.randint(SCREEN_HEIGHT - y_limitation[current_level-1][0] + self.area_move[0], SCREEN_HEIGHT - y_limitation[current_level-1][0] + self.area_move[1])


class rat(enemy):
    skin_1_Walk = [pygame.image.load('data/images/Enemys/Rats/Rat 1/L1.png'), pygame.image.load('data/images/Enemys/Rats/Rat 1/L2.png'), pygame.image.load('data/images/Enemys/Rats/Rat 1/L3.png'), pygame.image.load('data/images/Enemys/Rats/Rat 1/L4.png')]
    skin_1_Death = [pygame.image.load('data/images/Enemys/Rats/Rat 1/Death1.png'),pygame.image.load('data/images/Enemys/Rats/Rat 1/Death2.png'),pygame.image.load('data/images/Enemys/Rats/Rat 1/Death3.png'),pygame.image.load('data/images/Enemys/Rats/Rat 1/Death4.png')]
    skin_1 = [skin_1_Walk, skin_1_Death]
    
    skin_2_Walk = [pygame.image.load('data/images/Enemys/Rats/Rat 2/L1.png'), pygame.image.load('data/images/Enemys/Rats/Rat 2/L2.png'), pygame.image.load('data/images/Enemys/Rats/Rat 2/L3.png'), pygame.image.load('data/images/Enemys/Rats/Rat 2/L4.png')]
    skin_2_Death = [pygame.image.load('data/images/Enemys/Rats/Rat 2/Death1.png'),pygame.image.load('data/images/Enemys/Rats/Rat 2/Death2.png')]
    skin_2 = [skin_2_Walk, skin_2_Death]
    
    skins = [skin_1, skin_2]
    current_skin = skins[random.randint(0, len(skins)-1)]
    walk_Animation = current_skin[0]
    death_Animation = current_skin[1]
    walkCount = 0
    deathCount = 0
    death = False
    
    def __init__(self):                                         
         super().__init__(x = SCREEN_WIDTH, y = 0, area_move = [100, 150], health = 1, damage = 0, vel = 7)

       
    def draw(self, screen):
        if self.visible:
            if not (self.death):
                self.move()
                if self.walkCount + 1 >= 16:
                    self.walkCount = 0
           
                screen.blit(self.walk_Animation[self.walkCount //4], (self.x, self.y))
                self.walkCount += 1
            else:
                if self.current_skin == self.skin_2:
                    if self.deathCount < 4:
                        screen.blit(self.death_Animation[self.deathCount //2], (self.x, self.y))
                        self.deathCount += 1
                    else: 
                        self.deathh()
                        self.deathCount = 0
                else:
                    if self.deathCount < 8:
                        screen.blit(self.death_Animation[self.deathCount //2], (self.x, self.y))
                        self.deathCount += 1
                    else: 
                        self.deathh()
                        self.deathCount = 0
                    
            
            self.hitbox = (self.x, self.y, 25, 9)
            #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)


    def move(self):
       if self.x > -30:
            self.x -= self.vel
            
            
    def deathh(self):
        global score       
        score += 1
        self.health = 0
        slurpSounds.play()
        eatSounds[random.randint(0, len(eatSounds)-1)].play()
        
        
    def hit(self):
        hitSounds[random.randint(0, len(hitSounds)-1)].play()
        if self.health > man.damage:
            self.health -= man.damage
        else:
            self.death = True


    def update(self):
        self.death = False
        self.health = self.max_health
        self.current_skin = self.skins[random.randint(0, len(self.skins)-1)]
        self.walk_Animation = self.current_skin[0]
        self.death_Animation = self.current_skin[1]
        self.x = SCREEN_WIDTH
        self.y = random.randint(SCREEN_HEIGHT - y_limitation[current_level-1][0] + self.area_move[0], SCREEN_HEIGHT - y_limitation[current_level-1][0] + self.area_move[1])


class bird(enemy):
    skin_1_Walk = [pygame.image.load('data/images/Enemys/Birds/Bird 1/L1.png'), pygame.image.load('data/images/Enemys/Birds/Bird 1/L2.png'), pygame.image.load('data/images/Enemys/Birds/Bird 1/L3.png'), pygame.image.load('data/images/Enemys/Birds/Bird 1/L4.png'), pygame.image.load('data/images/Enemys/Birds/Bird 1/L5.png'), pygame.image.load('data/images/Enemys/Birds/Bird 1/L6.png')]
    skin_1_Death = [pygame.image.load('data/images/Enemys/Birds/Bird 1/Death1.png'), pygame.image.load('data/images/Enemys/Birds/Bird 1/Death2.png')]
    skin_1 = [skin_1_Walk, skin_1_Death]
    
    skin_2_Walk = [pygame.image.load('data/images/Enemys/Birds/Bird 2/L1.png'), pygame.image.load('data/images/Enemys/Birds/Bird 2/L2.png'), pygame.image.load('data/images/Enemys/Birds/Bird 2/L3.png'), pygame.image.load('data/images/Enemys/Birds/Bird 2/L4.png'), pygame.image.load('data/images/Enemys/Birds/Bird 2/L5.png'), pygame.image.load('data/images/Enemys/Birds/Bird 2/L6.png')]
    skin_2_Death = [pygame.image.load('data/images/Enemys/Birds/Bird 2/Death1.png')]
    skin_2 = [skin_2_Walk, skin_2_Death]
    
    skins = [skin_1, skin_2]
    current_skin = skins[random.randint(0, len(skins)-1)]
    walk_Animation = current_skin[0]
    death_Animation = current_skin[1]
    walkCount = 0
    deathCount = 0
    death = False
    
    def __init__(self):
         super().__init__(x = SCREEN_WIDTH, y = 0, area_move = [-100, -55], health = 1, damage = 0, vel = 12)

       
    def draw(self, screen):
        if self.visible:
            if not (self.death):
                self.move()
                if self.walkCount + 1 >= 12:
                    self.walkCount = 0
           
                screen.blit(self.walk_Animation[self.walkCount //2], (self.x, self.y))
                self.walkCount += 1
            else:
                if self.current_skin == self.skin_2:
                    if self.deathCount < 1:
                        screen.blit(self.death_Animation[self.deathCount //2], (self.x, self.y))
                        self.deathCount += 1
                    else: 
                        self.deathh()
                        self.deathCount = 0
                else:
                    if self.deathCount < 4:
                        screen.blit(self.death_Animation[self.deathCount //2], (self.x, self.y))
                        self.deathCount += 3
                    else: 
                        self.deathh()
                        self.deathCount = 0
            
            self.hitbox = (self.x, self.y, 38, 19)
            #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)


    def move(self):
       if self.x > -30:
            self.x -= self.vel
            
            
    def deathh(self):
        global score       
        score += 3
        self.health = 0
        slurpSounds.play()
        eatSounds[random.randint(0, len(eatSounds)-1)].play()
        
        
    def hit(self):
        hitSounds[random.randint(0, len(hitSounds)-1)].play()
        if self.health > man.damage:
            self.health -= man.damage
        else:
            self.death = True


    def update(self):
        self.death = False
        self.health = self.max_health
        self.current_skin = self.skins[random.randint(0, len(self.skins)-1)]
        self.walk_Animation = self.current_skin[0]
        self.death_Animation = self.current_skin[1]
        self.x = SCREEN_WIDTH
        self.y = random.randint(SCREEN_HEIGHT - y_limitation[current_level-1][0] + self.area_move[0], SCREEN_HEIGHT - y_limitation[current_level-1][0] + self.area_move[1])

        
class alkash(enemy):
    skin_1 = pygame.image.load('data/images/Enemys/Drunks/alkash L1.png')
    skin_2 = pygame.image.load('data/images/Enemys/Drunks/alkash2 L1.png')
    skins = [skin_1, skin_2]
    current_skin = skins[random.randint(0, len(skins)-1)]
    
    def __init__(self):
         super().__init__(x = SCREEN_WIDTH, y = 0, area_move = [0, 40], health = 10, damage = 1 * current_level, vel = 7)
       

    def draw(self, screen):
        if self.visible:
            screen.blit(self.current_skin, (self.x, self.y))
            self.hitbox = (self.x, self.y+23, 62, 10)
            #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)
            
            
    def hit(self):
        global score
        
        if self.health > man.damage:
            hitSounds[random.randint(0, len(hitSounds)-1)].play()
            self.health -= man.damage
        else:
            self.health = 0
            deathSound.play()
            fightSounds[random.randint(0, len(fightSounds)-1)].play()
            man.collisions = False
            score += 8


    def update(self):
        self.health = self.max_health
        self.current_skin = self.skins[random.randint(0, len(self.skins)-1)]
        self.x = SCREEN_WIDTH
        self.y = random.randint(SCREEN_HEIGHT - y_limitation[current_level-1][0] + self.area_move[0], SCREEN_HEIGHT - y_limitation[current_level-1][0] + self.area_move[1])

def load_level():
    global bgX0
    global bgX1
    global bgX2
    global time
    
    pygame.mixer.music.load('' + soundtracks[current_level-1])
    pygame.mixer.music.play(-1)
    bgX0 = backgrounds[current_level-1].get_width()*-1
    bgX1 = 0
    bgX2 = backgrounds[current_level-1].get_width()

def redrawGameWindow():
    global time
    global current_level
    
    draw_bg()
        
    if not (end_game):
        draw_text("ABTORNTET: " + str(score), 45, def_col, 180, 40)
        draw_text("LEVEL: " + str(current_level), 30, def_col, 80,90)
        col_change(def_col, col_dir)
        
        for enemy in enemys:
            enemy.draw(screen)
            
        man.draw(screen)
        
    if g == True:
            get_liminal_screen(backgrounds[current_level-1], bg0, 100)
            
    if liminal_screen:
        get_liminal_screen(backgrounds[current_level-1], bg0, 100)
        if alpha2 > 235 and current_level != final_level:
            draw_text("A  Game  About", 50, def_col, SCREEN_WIDTH//2, SCREEN_HEIGHT//2-75)
            draw_text("Real  man", 100, def_col, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            col_change(def_col, col_dir)
                
        if time == 1:
            if current_level < final_level - 1:
                pygame.mixer.music.load('data/Sounds/soundtracks/Sun Araw - Deep Cover.mp3')
                pygame.mixer.music.play()

            elif current_level == final_level - 1:
                pygame.mixer.music.fadeout(10000)
                
        elif time == 35 and current_level == final_level - 1:
            phoneCallSound.play()

#mainloop
man = player(600, SCREEN_HEIGHT - y_limitation[current_level-1][0])
enemys = []
alkash = alkash()
cat = cat()
rat = rat()
bird = bird()
pygame.time.set_timer(USEREVENT+3, random.randrange(2000, 3500))
new_game_button = button.Button(SCREEN_WIDTH // 2 - 225, SCREEN_HEIGHT // 2, start_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 - 310, SCREEN_HEIGHT // 2 + 100, load_img, 1)
play_button = button.Button(SCREEN_WIDTH // 2 - 360, SCREEN_HEIGHT // 2 + 100, play_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 200, exit_img, 1)
END_game_button = button.Button(SCREEN_WIDTH // 2 - 225, SCREEN_HEIGHT // 2, start_img, 1)
pause_count = 0
management = False
liminal_screen = False
fade = False
start_game = False
play_game = True
end_game = False
END = False
g = False
while play_game:
    
    clock.tick(FPS)
    if start_game == False:
        pygame.mouse.set_visible(True)
        screen.fill(def_col)
        col_change(def_col, col_dir)
        screen.blit(logo_menu, (SCREEN_WIDTH// 2 - 300, 25))
            
        if new_game_button.draw(screen):
            enemys.clear()
            score = 0
            current_level = 1
            d['level'] = current_level
            man = player(600, SCREEN_HEIGHT - y_limitation[current_level-1][0])
            load_level()
            management = True
            start_game = True
            
        if d['level'] > 1 and pause_count == 0:
            if load_button.draw(screen):
                score = 0
                current_level = d['level']
                man = player(600, SCREEN_HEIGHT - y_limitation[current_level-1][0])
                load_level()  
                management = True
                start_game = True
                
        if pause_count == 1:
            if play_button.draw(screen):
                current_level = d['level']
                load_level()
                management = True
                start_game = True

        if exit_button.draw(screen):
            d['level'] = current_level
            sys.exit()
       
    elif END == True:
        pygame.mouse.set_visible(True)
        screen.fill(def_col)
        col_change(def_col, col_dir)
        
        if END_game_button.draw(screen):
            sys.exit()
            
    else:
        #spawn enemy
        pygame.mouse.set_visible(False)
                    
        for enemy in enemys: 
             enemy.x += screen_scroll
             if enemy.x < -30: # If our obstacle is off the screen we will remove it
                 enemys.pop(enemys.index(enemy))
             if enemy.health <= 0: # If our obstacle is off the screen we will remove it
                 enemys.pop(enemys.index(enemy))
        if  alkash in enemys:   
            if man.hitbox[1] < alkash.hitbox[1] + alkash.hitbox[3] and man.hitbox[1] + man.hitbox[3] > alkash.hitbox[1] and man.hitbox[0] + man.hitbox[2] > alkash.hitbox[0] and man.hitbox[0] < alkash.hitbox[0] + alkash.hitbox[2]:
                man.collisions = True
            else:
                man.collisions = False
  
        if score >= 10 * current_level:
            if current_level != final_level:
                liminal_screen = True
                management = False
                if not (fade) and time > 0:
                    enemys.clear()
                    current_level += 1
                    d['level'] = current_level
                    man = player(600, SCREEN_HEIGHT - y_limitation[current_level-1][0])
                    orig_surf = backgrounds[current_level-1]
                    load_level()
                    score = 0
            else:
                if current_level == final_level and score >= (10 * current_level) + 6:
                    score = 56
                    
                    if g and time == 0:
                        END = True
                        score = 0
                        g = False
                        
                    if time < 99:
                        g = True
                        
                    management = False
                    pygame.mixer.music.fadeout(10000)
                    
                    if time > 35:
                        end_game = True
                        backgrounds[current_level-1].fill(def_col)
                    
                    if time == 56:
                        coughSounds[3].play()
        else:
            if time == 0:
                liminal_screen = False
                management = True
                
        redrawGameWindow()
    pygame.display.update()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_game = False

        if event.type == USEREVENT + 3 and management:
            rs = random.randrange(current_level * -1, 35)
            if rs < 0:
                coughSounds[random.randint(0, len(coughSounds)-2)].play()

        if event.type == USEREVENT + 3:
            r = random.randrange(0, 4)
            if r == 0 and cat not in enemys:
                cat.update()
                enemys.append(cat)
            elif r == 1 and alkash not in enemys:
                alkash.update()
                enemys.append(alkash)
            elif r == 2 and rat not in enemys:
                rat.update()
                enemys.append(rat)
            elif r == 3 and bird not in enemys:
                bird.update()
                enemys.append(bird)
                
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
        
    if management:
        if mouse[0]:
            for enemy in enemys: 
                if enemy.visible:
                    if man.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and man.hitbox[1] + man.hitbox[3] > enemy.hitbox[1]:
                        if man.hitbox[0] + man.hitbox[2] > enemy.hitbox[0] and man.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                            enemy.hit()
                            if enemy.damage > 0:
                                score -= random.randint(0, enemy.damage + 1)
                            
        if keys[pygame.K_a]: 
            if man.x > x_limitation:
                man.x -= man.vel  
            else:
                screen_scroll = man.vel
                bgX0 += screen_scroll
                bgX1 += screen_scroll
                bgX2 += screen_scroll  
    
            man.left = True
            man.right = False
            man.standing = False
       
        elif keys[pygame.K_d] and not (man.collisions):     
            if man.x <= SCREEN_WIDTH - x_limitation:
                man.x += man.vel
            else:
                screen_scroll = man.vel * -1
                bgX0 += screen_scroll
                bgX1 += screen_scroll
                bgX2 += screen_scroll  
    
            man.right = True
            man.left = False
            man.standing = False

        else:
            screen_scroll = 0
            man.standing = True
            man.walkCount = 0
        
        if not(man.isJump):
            if keys[pygame.K_SPACE] and current_level != final_level:
                man.isJump = True
                man.walkCount = 0
        else:
            if man.jumpCount >= -8:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * GRAVITY * neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 8     
  
        if keys[pygame.K_w] and man.y > SCREEN_HEIGHT - y_limitation[current_level-1][0]:
            man.y -= man.vel
            
        if keys[pygame.K_s] and man.y < SCREEN_HEIGHT - y_limitation[current_level-1][1] and not(man.isJump):
            man.y += man.vel
        
        if keys[pygame.K_ESCAPE]:
            pause_count = 1
            management = False
            start_game = False
            pygame.mixer.music.load('data/Sounds/soundtracks/Untitled.mp3')
            pygame.mixer.music.play(-1)
            
pygame.quit()

