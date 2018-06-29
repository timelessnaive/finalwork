# -*- coding: utf-8 -
import os, sys, pygame, random,time
from pygame.locals import *
from wxpy import *
pygame.init()
pygame.display.set_caption("My Space Shooter")
screen = pygame.display.set_mode((800, 600))
pygame.mouse.set_visible(100)#鼠标可见性，0为隐藏

#Background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((100,100,255))
#background.fill((random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)))
#Music
music=pygame.mixer.Sound("活在当下的少女.wav")
#Plane image
def get_plane(rect, color = (0, 0, 0)):
    surface = pygame.Surface(rect).convert()
    surface.fill(color)
    rect = surface.get_rect()
    return surface, rect

#Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color=(100, 255, 255)
        self.image, self.rect = get_plane((20, 20), self.color)
        self.rect.center = (400, 300)
        self.dx = 0
        self.dy = 0
        self.bullettimer = 0
        self.firespeed = 25#子弹发射间隔
        self.life = 5
        self.score = 0
        self.flag = 0
        self.time = 0
        self.st = 0
        self.st1 = 0
        self.f_s = [0]
        self.count = 0
        self.skill = 0
    def update(self):
        global background

        self.rect.move_ip((self.dx, self.dy))
        self.time = time.time()
        #Fire the bullet
        if self.bullettimer < self.firespeed:
            self.bullettimer += 1
        key = pygame.key.get_pressed()
        joystick_count = pygame.joystick.get_count()

        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            buttons = joystick.get_numbuttons()
            for i in range(buttons):
                button = joystick.get_button(i)
                if(i==0 and button and self.bullettimer == self.firespeed):#BUTTON A
                    bulletSprites.add(Bullet(self.rect.midtop))
                    self.bullettimer = 0

                if(i==2 and button and not self.flag ):#BUTTON X
                    self.firespeed = 5
                    self.bullettimer = 0
                    self.life -= 1
                    self.flag = 1
                    self.skill += 1
                    background.fill((255, 255, 51))
                    self.st = int(time.time())

        if(not (self.score % 10) and not(self.score in self.f_s)):
            self.life+=1
            self.f_s.append(self.score)

        if(self.flag==1):
            if((self.time - self.st)>=7):
                self.st = 0
                self.firespeed = 25
                self.bullettimer = 0
                background.fill((100, 100, 255))
                self.flag=2
                self.st1 = time.time()

        elif(self.flag==2):
            if(self.time-self.st1)>=8:
                self.flag=0

        if self.rect.left < 0:  #移动的左右限制
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800

        if self.rect.top <= 0:  #移动的上下限制
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

        if pygame.sprite.groupcollide(playerSprite, enemyBulletSprites, 0, 1):
            if(self.flag==1):
                self.count += 1
                self.score += 1
            else:
                self.life -= 1
        if pygame.sprite.groupcollide(playerSprite, enemySprites, 0, 1):
            if (self.flag==1):
                self.count += 1
                self.score += 2
            else:
                self.life -= 2
        if self.life <= 0:
            self.kill()
            pass
        if pygame.sprite.groupcollide(bulletSprites, enemySprites, 0, 1):
            self.score+=2
    '''
    def reset(self):
        self.rect.bottom = 600
        if(self.flag):
            self.firespeed = 0
        elif(not self.flag):
            self.firespeed = 25
    
    def firespeed_up(self):
        self.firespeed -= 5
        if self.firespeed <= 5:
            self.firespeed = 5
    '''

class Enemy(pygame.sprite.Sprite):
    def __init__(self,centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = get_plane((20,20),(150,150,255))
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()

        self.counter += 1
        if self.counter >= 60:
            enemyBulletSprites.add(EnemyBullet(self.rect.midbottom))
            self.counter = 0

    def reset(self):
        self.counter = random.randint(0, 60)
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(1, 4)
        self.dx = random.randrange(-2, 2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect = get_plane((x, y),(255,255,255))
        self.image, self.rect = get_plane((5, 5), (255, 255, 255))
        self.rect.center = pos
        self.x = 0
        self.y = 0

    def update(self):
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            axes = joystick.get_numaxes()
            for i in range(axes):
                axis = joystick.get_axis(i)
                #if(self.x and self.y):
                if (i == 3):
                    self.y = axis * 10
                elif (i == 4):
                    self.x = axis * 10

        if self.rect.top < 0:
            self.kill()
        else:
            self.rect.move_ip(self.x, self.y)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = get_plane((5, 5),(150,150,255))
        self.rect.center = pos
        self.x = random.randrange(0, 5)  # 敌人的子弹会抖
        self.y = random.randrange(0, 5)
    def update(self):
        if self.rect.top < 0:
            self.kill()
        else:
            self.rect.move_ip(self.x, self.y)

class SpaceMenu:

    def __init__(self, *options):
        self.options = options
        self.x = 0
        self.y = 0
        self.font = pygame.font.Font(None, 32)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [0, 0, 0]
        self.height = len(options)*self.font.get_height()
        for i in options:
            text = i[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    def draw(self, surface):
        i = 0
        for j in self.options:
            if i == self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = j[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, (self.x, self.y + i * self.font.get_height()))
            i += 1

    def update(self):
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            buttons = joystick.get_numbuttons()

            axes = joystick.get_numaxes()
            for i in range(axes):
                axis = joystick.get_axis(i)
                if (i == 1 and axis > 0.5):
                    self.option += 1
                    time.sleep(0.2)
                elif (i == 1 and axis < -0.5):
                    self.option -= 1
                    time.sleep(0.2)
            for i in range(buttons):
                button = joystick.get_button(i)
                if (i == 0 and button):
                    self.options[self.option][1]()
            if self.option > len(self.options) - 1:
                self.option = 0
            elif self.option < 0:
                self.option = len(self.options) - 1
    '''
    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP or e.key == pygame.K_w:
                    self.option -= 1
                elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
                    self.option += 1
                elif e.key == pygame.K_RETURN:
                    self.options[self.option][1]()
            if self.option > len(self.options) - 1:
                self.option = 0
            elif self.option < 0:
                self.option = len(self.options) - 1
    '''


    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_font(self, font):
        self.font = font
        for i in self.options:
            text = i[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    def set_highlight_color(self, color):
        self.hcolor = color

    def set_normal_color(self, color):
        self.color = color

    def center_at(self, x, y):
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)

def game():
    player = Player()
    font = pygame.font.Font(None,32)

    global playerSprite
    playerSprite = pygame.sprite.RenderPlain((player))

    global enemySprites
    enemySprites = pygame.sprite.RenderPlain(())
    enemySprites.add(Enemy(200))
    enemySprites.add(Enemy(300))
    enemySprites.add(Enemy(400))

    global bulletSprites
    bulletSprites = pygame.sprite.RenderPlain(())

    global enemyBulletSprites
    enemyBulletSprites = pygame.sprite.RenderPlain(())
    last_life = 0
    clock = pygame.time.Clock()
    counter = 0
    keepGoing = True


    bot = Bot()
    music.play()
    starttime = time.time()
    while keepGoing:
        clock.tick(30)
        #Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                music.stop()

            joystick_count = pygame.joystick.get_count()

            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                buttons = joystick.get_numbuttons()
                axes = joystick.get_numaxes()
                for i in range(axes):
                    axis = joystick.get_axis(i)
                    if(i==1 and axis>0.5):
                        player.dy = 10
                    elif(i==1 and axis<-0.5):
                        player.dy = -10
                    elif(i==0 and axis<-0.5):
                        player.dx = -10
                    elif(i==0 and axis>0.5):
                        player.dx = 10


                    if (i == 1 and axis < 0.5 and axis > 0):
                        player.dy = 0
                    elif (i == 1 and axis > -0.5 and axis < 0):
                        player.dy = 0
                    elif (i == 0 and axis > -0.5 and axis < 0):
                        player.dx = 0
                    elif (i == 0 and axis < 0.5 and axis > 0):
                        player.dx = 0
                for i in range(buttons):
                    button = joystick.get_button(i)
                    if (i == 1 and button ):  # BUTTON B
                        keepGoing=False
                        music.stop()

                '''
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.dy = -10
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.dy = 10
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.dx = -10
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.dx = 10
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.dy = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.dy = 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.dx = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.dx = 0
                '''
        #Update
        screen.blit(background, (0,0))
        playerSprite.update()
        enemySprites.update()
        bulletSprites.update()
        enemyBulletSprites.update()

        #sent="你击败了{0}个敌人，使用了{1}次技能，存活时间{2}秒".format(player.count,player.skill,timewent)

        timewent=int(player.time-starttime)
        '''
        #---------------------
        if(timewent%60==0 and player.score<=(timewent-20)):
            player.life=0
        #---------------------
        '''
        if(last_life!= player.life and player.life<=1):
           bot.file_helper.send("你的生命已如风中残烛！")
        last_life=player.life

        text = "LIFE:" + str(player.life)
        text2="TIME:" + str(timewent)
        text1 = "SCORE:" + str(player.score)
        #text1 = "dx:" + str(player.dx)
        #test =  "TEST:"+ str(player.flag)+" "+str(int(player.time-player.st))+" "+str(int(player.time-player.st1))
        if(player.flag==1):
            power =  (7-int(player.time-player.st))*2*"|"
            power1 = font.render(power, True, (255, 255, 255))
            screen.blit(power1, (0, 80))
        elif (player.flag==2):
            power = int(player.time-player.st1) * 2 * "|"
            power1 = font.render(power, True, (255, 255, 255))
            screen.blit(power1, (0, 80))
        else:
            power = 14*"|"
            power1 = font.render(power, True, (255, 255, 255))
            screen.blit(power1, (0, 80))

        life = font.render(text, True, (255,255,255))
        score = font.render(text1, True, (255,255,255))
        time1 = font.render(text2, True, (255,255,255))
        #test1 = font.render(test, True, (255,255,255))

        playerSprite.draw(screen)
        enemySprites.draw(screen)
        bulletSprites.draw(screen)
        enemyBulletSprites.draw(screen)

        screen.blit(life,  (0, 0))
        screen.blit(score, (0, 20))
        screen.blit(time1, (0, 40))
        #screen.blit(test1, (0, 60))

        pygame.display.flip()

        counter += 1
        if counter >= 20 and len(enemySprites) < 20:
            enemySprites.add(Enemy(300))
            counter = 0

        #if game over
        if len(playerSprite) == 0:
            if(player.score<=10):
                sent="你的分数太低了！我拒绝发送这样低的数据"
            elif(player.score<=30):
                sent="获得了{0}分，使用了{1}次技能，存活时间{2}秒,年轻人还是naive啊".format(player.score, player.skill, timewent)
            elif(player.score<=100):
                sent = "你获得了{0}分，使用了{1}次技能，存活时间{2}秒，你们年轻人还是too young to simple,sometimes naive.".format(player.score,player.skill,timewent)
            else:
                sent="大佬收下我的膝盖吧"
            bot.file_helper.send(sent)
            gameOver()
            keepGoing = False

def gameOver():
    #Game over screen
    #----------bug--------
    #global bot
    #bot.file_helper.send(welcome)
    #---------------------
    menuTitle = SpaceMenu(
            ["GAME OVER"])
    menuTitle.set_font(pygame.font.Font(None, 80))
    menuTitle.center_at(400,230)
    menuTitle.set_highlight_color((255,255,255))
    music.stop()
    info = SpaceMenu(
            ["Press B back to menu"])
    info.set_font(pygame.font.Font(None, 40))
    info.center_at(400,350)
    info.set_highlight_color((255,255,255))

    keepGoing = True
    while keepGoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                music.stop()
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                buttons = joystick.get_numbuttons()
                for i in range(buttons):
                    button = joystick.get_button(i)
                    if (i == 1 and button ):  # BUTTON B
                        keepGoing=False
                        music.stop()
        '''       
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    music.stop()
            elif event.type == pygame.QUIT:
                keepGoing = False
                music.stop()
        '''
        menuTitle.draw(screen)
        info.draw(screen)
        pygame.display.flip()

def aboutMenu():
    '''
    bot = Bot()
    welcome = "小游戏要开始了哦！"
    bot.file_helper.send(welcome)
    '''
    menuTitle = SpaceMenu(
        ["BATTLE WITH BLOCK"])

    info = SpaceMenu(

        [""],
        ["WRITER"],
        [""],
        ["Wang Zhihao"],
        [""]
        ["PRESS B TO RETURN"])

    menuTitle.set_font(pygame.font.Font(None, 60))
    menuTitle.center_at(400, 150)
    menuTitle.set_highlight_color((255, 255, 255))

    info.center_at(400, 320)
    info.set_highlight_color((255, 255, 255))
    info.set_normal_color((200, 200, 255))

    clock = pygame.time.Clock()
    keepGoing = True

    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    music.stop()
            elif event.type == QUIT:
                keepGoing = False

        screen.blit(background, (0,0))
        menuTitle.draw(screen)
        info.draw(screen)
        pygame.display.flip()

def option1():
    game()
def option2():
    aboutMenu()
def option3():
    pygame.quit()
    sys.exit()

#Main
def main():
    menuTitle = SpaceMenu(
        ["BATTLE WITH BLOCK"])
        #["方块大战"])
    menu = SpaceMenu(
        ["GO", option1],
        ["ABOUT THE GAME", option2],
        ["EXIT", option3])
        #["开始游戏", option1],
        #["微信登录", option2],
        #["退出", option3])

    menuTitle.set_font(pygame.font.Font(None, 60))
    menuTitle.center_at(400, 150)
    menuTitle.set_highlight_color((255, 255, 255))
    menu.center_at(400, 320)
    menu.set_highlight_color((255, 255, 255))
    menu.set_normal_color((200, 200, 255))

    clock = pygame.time.Clock()
    keepGoing = True

    while True:
        clock.tick(30)
        events = pygame.event.get()
        menu.update()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                return
        screen.blit(background, (0, 0))
        menu.draw(screen)
        menuTitle.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()