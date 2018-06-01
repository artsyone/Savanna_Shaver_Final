
# Imports
import pygame
import random

# Initialize game engine
pygame.init()



# Window
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "FOOTBALL!!!!"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

     
# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)
DARKGREEN = (1,63,30)


# Fonts
FONT_SM = pygame.font.Font("fonts/nums.ttf", 24)
FONT_LG = pygame.font.Font("fonts/score.ttf", 64)
FONT_MD = pygame.font.Font(None, 32)
FONT_XL = pygame.font.Font("fonts/sports.ttf", 96)
MY_FONT = pygame.font.Font(None,30)
myfont = pygame.font.SysFont("monospace", 16)


# Images
ship_img = pygame.image.load('images/p1backp.png')
enemy = pygame.image.load('images/p1fronty.png')
laser_img = pygame.image.load('images/bullet.png')
field = pygame.image.load("images/footballfield1.png")
bomb_img  = pygame.image.load("images/p1fronty.png")
enemy_img = pygame.image.load('images/p1back.png')
crowds = pygame.image.load('images/watchfootball.jpg')
winner = pygame.image.load('images/winner.png')
thing1 = pygame.image.load('images/mob4.png')
thing2 = pygame.image.load('images/mob3.png')
thing3 = pygame.image.load('images/mob0.png')
lose = pygame.image.load('images/footlose2.jpg')
p1dam = pygame.image.load('images/p1backdam.png')
p2dam = pygame.image.load('images/p1backdam2.png')
p3dam = pygame.image.load('images/p1backdam3.png')

p4dam = pygame.image.load('images/p1backdam4.png')
p5dam = pygame.image.load('images/p1backdam5.png')
md = pygame.image.load('images/mobdam.png')
md1 = pygame.image.load('images/mobdam1.png')
md2 = pygame.image.load('images/mobdam2.png')

#sounds

theme = pygame.mixer.music.load("sounds/theme.ogg")
sad = pygame.mixer.Sound("sounds/sad.ogg")
ouch = pygame.mixer.Sound("sounds/ouch.ogg")
theme = pygame.mixer.Sound("sounds/theme.ogg")
bombbam = pygame.mixer.Sound("sounds/hitabomb.ogg")
oof = pygame.mixer.Sound("sounds/oof.ogg")
yeah = pygame.mixer.Sound("sounds/ohyeah.ogg")

run = False


START = 0
PLAYING = 1
END = 2        

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 5

        self.cooldown = [15,15]

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

     

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        
        lasers.add(laser)
        
       

    def update(self, bombs,mobs,player):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)
       

        for hit in hit_list:
            
            ouch.play()
            player.shield -= 20   


        if player.shield == 80:
            self.image = p1dam
        if player.shield == 60:
            self.image = p2dam
        if player.shield == 40:
            self.image = p3dam
        if player.shield == 20:
            self.image = p5dam
        if player.shield == 0:
            self.image = p5dam
        hit_list = pygame.sprite.spritecollide(self, mobs, False)
        if len(hit_list) > 0:
            self.shield = 0 

        if player.shield == 0:
            sad.play()
            self.kill()

        if self.cooldown[0] != self.cooldown[1]:
            self.cooldown[0] += 1 


        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH

       
    
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0 :
            self.kill()
    
class Mob(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        

    def update(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)
        
        if len(hit_list) > 0:
            oof.play()
            player.score += 1
            for e in  receivers:
                e.rect.y += 50
    def lost(self):
          return self.rect.y >= 665
        
class Mobagain(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = 3
        self.mask = pygame.mask.from_surface(image)

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        

    def update(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)
        for hit in hit_list:
            ouch.play()
            self.shield -= 1

        if self.shield == 2:
            self.image = md1
        if self.shield == 1:
            self.image = md2
       
          
        
        if len(hit_list) > 0:
            oof.play()
            player.score += 3
            for e in  receivers:
                e.rect.y += 150
               
        if self.shield == 0:
           yeah.play()
           self.kill()

           
    def lost(self):
          return self.rect.y >= 665
  

class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        
        self.speed = 3

    def update(self,lasers,player):
        self.rect.y += self.speed

        if self.rect.top >= HEIGHT :
            self.kill()
          
        hit_list = pygame.sprite.spritecollide(self, lasers, True)

        if len(hit_list) > 0:
            bombbam.play()
            player.score += 1
            self.kill()

class Team(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 5
                      
    def update(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)
    
        if len(hit_list) > 0:
             
            
            for e in  receivers:
                  if level == 0:
                      e.rect.y -= 300
                  elif level == 1: 
                    e.rect.y -= 200
                   
                  elif level == 2:
                    e.rect.y -= 100
                    
                  elif level == 3: 
                    e.rect.y -= 75
                  elif level == 4: 
                    e.rect.y -= 50
                  elif level == 5: 
                    e.rect.y -= 20
                   
                   
                  else:

                      if level < 5:
                          e.rect.y -= 10
                      else: 
                          e.rect.y -= 300

    def has_scored(self):
        return self.rect.y <= 0

    def has_lost(self):
      
        return self.rect.y >= 800
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.bomb_rate = 60

        self.speed = 3
        self.moving_right = True
        
    def move(self):
       
        reverse = False
        if self.moving_right:
            
            for m in  mobs:
                m.rect.x += self.speed
                
                if m.rect.right >= WIDTH:
                    reverse = True
        else:
               
            for m in  mobs:
                m.rect.x -= self.speed
                if m.rect.left <= 0:
                    reverse = True

        if reverse:  
                self.moving_right = not self.moving_right
                
                for m in mobs:
                    m.rect.y += 50
         
    def choose_bomber(self):
            rand = random.randrange(0, self.bomb_rate)
            all_mobs = mobs.sprites()
            
            if len(all_mobs) > 0 and rand == 0:
                return random.choice(all_mobs)
            else:
                return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

        run == []  
              
class FleetT:
    def __init__(self, receivers):
        self.receivers = receivers
        self.speed = 3
        self.moving_right = True
        
    def move(self):
        
            reverse = False
        
            if self.moving_right:
            
                for e in  receivers:
                    e.rect.x += self.speed
                
                
                    if e.rect.right >= WIDTH:
                        reverse = True

            else:
           
                for e in receivers:
                    e.rect.x -= self.speed
                    if e.rect.left <= 0:
                        reverse = True
        
            
            if reverse:  
                self.moving_right = not self.moving_right
                
                for e in receivers:
                    e.rect.x += 0
          
    def update(self):
        self.move()

# Make game objects
 
def mobbyboys(mobs):
    mob1 = Mob (123,65,enemy)
    mob2 = Mob (223,65,enemy)
    mob3 = Mob (323,65,enemy)
    mob4 = Mob (423,65,enemy)

    mob5 = Mobagain (0,165,thing3)
    mob6 = Mobagain (250,165,thing1 )
    mob7 = Mobagain (500,165,thing2)

    mobs.empty()
    mobs.add(mob1,mob2,mob3,mob4,mob5,mob6,mob7)

# Make sprite groups
player = pygame.sprite.GroupSingle()
lasers = pygame.sprite.Group()
mobs = pygame.sprite.Group()
receivers = pygame.sprite.Group()
bombs = pygame.sprite.Group()

# Make fleet
fleet = Fleet(mobs)
fleetT = FleetT(receivers)

# set stage
stage = START

# Game helper functions

def setup():
    global stage,ship,receivers, player,level 
    stage = START
    ship = Ship(384, 736, ship_img)
    
    player.add(ship)

    team1 = Team (123,564,enemy_img)
    team2 = Team (256,564,enemy_img)
    team3 = Team  (364,564,enemy_img)

    receivers.empty()
    receivers.add(team1,team2,team3)

    mobbyboys(mobs)

    player.score = 0
    player.shield = 100

    level = 0
    
def levelup():
    
    global stage,ship,receivers, player,level
    ship = Ship(384, 736, ship_img)
    stage = PLAYING
    player.add(ship)

    team1 = Team (123,564,enemy_img)
    team2 = Team (256,564,enemy_img)
    team3 = Team  (364,564,enemy_img)

    receivers.empty()
    receivers.add(team1,team2,team3)

    mobbyboys(mobs)
    
def show_title_screen():
    
    screen.blit(crowds,(0,0))
    title_text = FONT_XL.render("FOOTBALL!", 1, RED)
    screen.blit(title_text, [208, 350])

def show_stats(player):
    
    #score_text = FONT_MD.render("Score:", 1, RED)
    #screen.blit(score_text, [32, 32])
    score_text = FONT_LG.render(str(player.score), 1, DARKGREEN)
    screen.blit(score_text, [32, 82])

    shield_text = FONT_SM.render(str(player.shield), 1, DARKGREEN)
    screen.blit(shield_text, [135, 32])

    pygame.draw.rect(screen, WHITE, [32,32,100,25])
    pygame.draw.rect(screen, GREEN, [32,32,(player.shield),25])
    lev_text = FONT_SM.render("Level:", 1, DARKGREEN)
    screen.blit(lev_text, [32, 62])
    level_text = FONT_SM.render(str(level), 1, DARKGREEN)
    screen.blit(level_text, [92, 64])
    
def show_end_screen():
    
    screen.fill(BLACK)
    screen.blit(lose,(0,0))
    title_text = FONT_XL.render("FOOTBALL!", 1, RED)
    score_text = FONT_LG.render(str(player.score), 1, RED)
    screen.blit(score_text, [22, 32])
 
    playagain_text = FONT_SM.render("To play again press R ", 1, DARKGREEN)
    screen.blit(playagain_text, [110, 32])

    end_text = FONT_SM.render("To quit the game press X " , 1, DARKGREEN)
    screen.blit(end_text, [110, 62])

    stats_text = FONT_SM.render("To see stats press S  " , 1, DARKGREEN)
    screen.blit(stats_text, [110,92])

    lose_text = FONT_LG.render("GAME OVER" , 1, DARKGREEN)
    screen.blit(lose_text, [715, 32])


def game_stats():
    global name
    
    name = input("To begin insert your initials:")
    
    f = open('name.txt','a')
    f.write('\n' + (name))
    f.close()

def stat_ts():
    score2 = player.score
  
    f = open('score.txt','a')
    f.write('\n' + str(score2))
    
def stats_write():
                         
    with open('name.txt', 'r') as f:
      words = f.read().splitlines()               
                    
    with open('score.txt', 'r') as f:
     s_words = f.read().splitlines()
                    
    data_file = 'score.txt'
                
    with open(data_file, 'r') as f:
     lines = f.read().splitlines()

    pygame.draw.rect(screen, RED, [0,0,800,600])
    text1 = MY_FONT.render(("Name"), True, WHITE)
    screen.blit(text1, [125, 100])
               
    text3 = MY_FONT.render(("Score"), True, WHITE)
    screen.blit(text3, [325, 100])

    text4 = MY_FONT.render(str((words[-6])), True, WHITE)
    screen.blit(text4, [125, 150])
                
    text11 = MY_FONT.render(str(s_words[-6]), True, WHITE)
    screen.blit(text11, [325, 150])

    text4 = MY_FONT.render(str((words[-5])), True, WHITE)
    screen.blit(text4, [125, 200])
    text11 = MY_FONT.render(str(s_words[-5]), True, WHITE)
    screen.blit(text11, [325, 200])

    text4 = MY_FONT.render(str((words[-4])), True, WHITE)
    screen.blit(text4, [125, 250])
                
    text11 = MY_FONT.render(str(s_words[-4]), True, WHITE)
    screen.blit(text11, [325, 250])
                
    text4 = MY_FONT.render(str((words[-3])), True, WHITE)
    screen.blit(text4, [125, 300])
                
    text11 = MY_FONT.render(str(s_words[-3]), True, WHITE)
    screen.blit(text11, [325, 300])
                
    text4 = MY_FONT.render(str((words[-2])), True, WHITE)
    screen.blit(text4, [125, 350])
                
    text11 = MY_FONT.render(str(s_words[-2]), True, WHITE)
    screen.blit(text11, [325, 350])
                
    text8 = MY_FONT.render((name), True, WHITE)
    screen.blit(text8, [125, 500])
                
    text10 = MY_FONT.render(str((player.score)), True, WHITE)
    screen.blit(text10, [325, 500])

    highscore_text = FONT_SM.render("HIGHSCORE" , 1, DARKGREEN)
    screen.blit(highscore_text, [550, 92])

    with open('highscore.txt', 'r') as f:
      score = f.read().splitlines()
      
      text1 = FONT_LG.render(str(score[-1]), True, WHITE)
      screen.blit(text1, [570, 120])

      highscore = str(score[-1])
      
    new_highscore = []
    if str(player.score) > highscore:
        new_highscore = player.score
        f = open('highscore.txt','a')
        f.write('\n' + str(new_highscore))
        
# Game loop
levelup()
setup()
game_stats()
stats = False
done = False
pygame.mixer.music.play(-1)

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            if event.key == pygame.K_x:
                    done = True
            if stage == END:
                if event.key == pygame.K_s:
                    stats = not stats
                    stat_ts()
                if event.key == pygame.K_r:
                    
                    setup()
                            
    if stage == PLAYING:
        
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
             ship.move_left()
        elif pressed[pygame.K_RIGHT]:
             ship.move_right()

    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
            player.update(bombs,mobs,player)
            lasers.update()
            bombs.update(lasers,player)
            mobs.update(lasers)
            receivers.update(lasers)
            fleet.update()
            fleetT.update()
            
            if player.shield <= 0:
                stage = END
                
    for t in receivers: 
        if t.has_lost():
            stage = END

    more = False            
    for t in receivers: 
        if t.has_scored():
            more = True

    for m in mobs: 
        if m.lost():
            stage = END
            
    if more:
        level += 1
        levelup()
    

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    
    screen.blit(field,(0,20))
    pygame.draw.rect(screen, RED, [0,0,1000,50])
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    receivers.draw(screen)

    show_stats(player)

    if stage == START:
        
        show_title_screen()

    if stage == END:
       
        show_end_screen()

        if stats:
                
            stats_write()
        
    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()
