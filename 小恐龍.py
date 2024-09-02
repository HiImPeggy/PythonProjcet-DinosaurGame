# -*- coding: utf-8 -*-
"""
Created on Sun May 14 22:03:15 2023

@author: blodg
"""

import pygame
import sys
import os
import random

width = 1100;   height = 500

case = 0


class Text:
    def __init__(self, text, size, color, position=(0, 0)):
        self.font = pygame.font.SysFont('freesansbold.ttf', size)  # 字體大小(參數)與字型
        self.surface = self.font.render(text, True, color)  # 印出的字串(參數)與呈現
        self.rect = self.surface.get_rect()  # 文字框起
        self.rect.center = position  # 文字的中心位置(參數)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

class dinosaur(pygame.sprite.Sprite):
    X_POS = 80
    Y_POS = 300
    Y_POS_DUCK = 340
    JUMP_VEL = 7
    global rocket_x;  global rocket_y
    global flag
    
    run_img_list = []
    duck_img_list = []
    jump_img = []
    dead = []
    
    # 初始化
    def __init__(self,case):

        # 定義變數
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.dino_shoot = False
        self.step_index = 0  # 腳步動畫
        self.jump_vel = self.JUMP_VEL  # 跳上、下的速度
        self.case = case
        
        # Load 圖檔
        for root, dirs, files in os.walk('./dino'):
            for file in files:
                if case == 0:
                    if 'b_' not in file:
                        if 'Run' in file:
                            self.run_img_list.append(pygame.image.load(root+'/'+file))
                        if 'Jump' in file:
                            self.jump_img.append(pygame.image.load(root+'/'+file))
                        if 'Duck' in file:
                            self.duck_img_list.append(pygame.image.load(root+'/'+file))
                        if 'Dead' in file:
                           self.dead.append(pygame.image.load(root+'/'+file))
                else:
                    if 'b_'  in file:
                        if 'Run' in file:
                            self.run_img_list.append(pygame.image.load(root+'/'+file))
                        if 'Jump' in file:
                            self.jump_img.append(pygame.image.load(root+'/'+file))
                        if 'Duck' in file:
                            self.duck_img_list.append(pygame.image.load(root+'/'+file))
                        if 'Dead' in file:
                            self.dead.append(pygame.image.load(root+'/'+file))
                            

        self.image = self.run_img_list[0]  # 恐龍跑的第一步

        # 把恐龍腳色框列
        
        self.rocket = pygame.image.load('./picture/rocket.png')
        self.rocket_rect = self.image.get_rect()
        
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.shoot_vel = 5
        self.tmp_y = self.Y_POS
        
        if case == 0:
            self.Y_POS = 350

    def run(self):
        self.image = self.run_img_list[self.step_index // 5]  # 依 step_index 決定恐龍的跑步圖片，每五個step_index換一張圖
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img_list[self.step_index // 5]  # 依 step_index 決定恐龍的蹲下圖片，每五個step_index換一張圖
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        if self.case == 0:
            self.dino_rect.y = self.Y_POS_DUCK + 50
        else:
            self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1
        
      
    def jump(self):
        self.image = self.jump_img[0]
        if self.dino_jump:
              # 依目前的跳躍速度來移動小恐龍的y座標值
            if self.case == 0:
                self.dino_rect.y -= self.jump_vel * 4
                self.jump_vel -= 0.41  # 若jump_vel小於0則代表小恐龍逐漸往下掉
            else:
                self.dino_rect.y -= self.jump_vel * 3.5
                self.jump_vel -= 0.35
                
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
        
        
    def shoot(self):
        
        
        self.rocket = pygame.image.load('./picture/rocket.png')

        if self.dino_shoot:
            
            self.rocket_rect.x  = self.dino_rect.x + self.shoot_vel * 3
            
            if self.rocket_rect.x < 1100 :  
                # print(self.pos_x)
                self.shoot_vel += 3
                self.sdraw(screen)
            
            else:  
                # print(self.pos_x)
                self.dino_shoot = False  
                self.shoot_vel = 5
                # print(self.dino_shoot)
         

       
    # 更新動作
    def update(self, user_input : pygame.key ):
        
        global rocket_num
        
        if user_input[pygame.K_RIGHT] and not self.dino_shoot and rocket_num > 0:
            if not self.dino_shoot :   
                if self.case == 1:
                    self.rocket_rect.y = self.dino_rect.y + 20
                else:
                    self.rocket_rect.y = self.dino_rect.y + 10
            rocket_num -= 1    
            self.dino_shoot = True
            self.shoot_vel = 6
            
            
        
        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or user_input[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
            

        # 以變數判斷小恐龍目前該做甚麼動作
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0
        if self.dino_shoot:
            self.shoot()
        else:
            self.rocket_rect.x  = 0
            self.rocket_rect.y  = 0

    def draw(self, screen : pygame.display):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
            
    def sdraw(self, screen : pygame.display):
        screen.blit(self.rocket, (self.rocket_rect.x, self.rocket_rect.y ))
        # pygame.display.update()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, imageList : list, typeObject : int):

        self.image_list = imageList  # 以變數儲存障礙物類型
        self.type = typeObject  # 以變數儲存障礙物樣貌
        self.rect = self.image_list[self.type].get_rect()  # 將障礙物框起
        self.rect.x = width  # 障礙物X座標位置

    def update(self):
        self.rect.x -= game_speed

    def draw(self, screen : pygame.display):
        screen.blit(self.image_list[self.type], (self.rect.x, self.rect.y))

class Prize(Obstacle):
    def __init__(self, image_list : list):
        pygame.sprite.Sprite.__init__(self)
        self.type = 0 # 三種大仙人掌型態隨機選取一種
        super().__init__(image_list, self.type)  # 繼承障礙物屬性與動作
        self.rect.y = random.randint(20, 330)  # Y座標位置
        self.rect.x = random.randint(700, 1000)
        
class LargeCactus(Obstacle):
    def __init__(self, image_list : list):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.randint(0, 2)  # 三種大仙人掌型態隨機選取一種
        super().__init__(image_list, self.type)  # 繼承障礙物屬性與動作
        self.rect.y = 330  # Y座標位置

class SmallCactus(Obstacle):
   
    def __init__(self, image_list : list):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.randint(0, 1)  # 三種小仙人掌型態隨機選取一種
        super().__init__(image_list, self.type)  # 繼承障礙物屬性與動作
        self.rect.y = 350  # Y座標位置


class Bird(Obstacle):
    global case
    
    def __init__(self, image_list : list):
        pygame.sprite.Sprite.__init__(self)
        self.type = 0  # 設置樣貌變數用以回傳
        super().__init__(image_list, self.type)  # 繼承障礙物屬性與動作
        if case == 0:
            self.rect.y = 285
        else:
            self.rect.y = 250  # Y座標位置
        self.index = 0  # 設置決定翼龍飛行型態之變數

    def draw(self, screen : pygame.display):
        if self.index >= 10:
            self.index = 0
        screen.blit(self.image_list[self.index // 5], self.rect)  # 以index決定飛行的動作，每五個index為一種飛行動作
        self.index += 1


def play(case):
    global width;   global height
    global game_speed;  global flag
    flag = False
    game_speed = 8    # 背景移動速度
    x_pos_bg = 0    # 背景x座標
    y_pos_bg = 0
    
    day = pygame.image.load("./picture/day.png")
    night = pygame.image.load("./picture/night_2.png")
    smoke = pygame.image.load("./picture/smoke.png")
    prize = [ pygame.image.load("./picture/pri.png")]
    
    pygame.mixer.music.load("bgm.mp3") 
    
    pygame.mixer.music.play(-1, 0) 
    
    
    SMALL_CACTUS = [pygame.image.load('./picture/s_cactus1.png'),
                    pygame.image.load('./picture/s_cactus2.png'),]

    LARGE_CACTUS = [pygame.image.load('./picture/L_cactus1.png'),
                    pygame.image.load('./picture/L_cactus2.png'),
                    pygame.image.load('./picture/L_cactus3.png'),]
    
    BIRD = [pygame.image.load('./picture/Bird1.png'),pygame.image.load('./picture/Bird2.png'),]
    rocket = pygame.image.load('./picture/rocket.png')
    
    # 分數(變數)
    global points
    global rocket_num
    rocket_num = 10
    points = 0

    time = 0
    # 時鐘(變數)
    clock = pygame.time.Clock()
   
    # 小恐龍(變數)
    player = dinosaur(case)
    change = 1
    
    # 障礙物串列
    obstacles = []
    
    tmp_x = 0;   tmp_y = 0
    
    run = True
    while  run:
        # background move
        time += 1
        if points % 1000 == 0:
            
            change += 1
        
        if change % 2 == 0:
            bgd = day
        else:
            bgd = night
            
        image_width = bgd.get_width()
        
            
        screen.blit(bgd, (x_pos_bg, y_pos_bg))
        screen.blit(bgd, (image_width + x_pos_bg, y_pos_bg))
        
        x_pos_bg -= game_speed  # 使背景移動
        if x_pos_bg <= -image_width:
            screen.blit(bgd, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text_position = (1000, 40)
        
        if change % 2 == 0:
            text = Text("Points: " + str(points), 30, 'black', text_position)
            text_r = Text(': '+str(rocket_num), 40, 'black', (130,40))
            
        else:
            text = Text("Points: " + str(points), 30, 'white', text_position)
            text_r = Text(': '+str(rocket_num), 40, 'white', (130,40))
            
        screen.blit(rocket, (-45, -45))
        
        text.draw(screen)
        text_r.draw(screen)
        
        
        # 小恐龍
        
        user_input = pygame.key.get_pressed()  # 接收玩家指令

        # print(user_input)
        player.update(user_input)  # 依據玩家指令更新恐龍的動作
        player.draw(screen)  # 將恐龍換上
        # player.sdraw(screen)
        
        if len(obstacles) == 0:
            rand = random.randint(0, 3)
            # print(rand)
            if rand == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rand == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif rand == 2:
                obstacles.append(Bird(BIRD))
            elif rand == 3:
                obstacles.append(Prize(prize))
        
        if flag :
            rocket_num += 1
            flag = False
            
            
        # p = Prize(prize,random.randint(0,2200), random.randint(0,500))
        for obstacle in obstacles:
            
            obstacle.update()  # 障礙物移動
            obstacle.draw(screen)  # 更新動畫
              
            if player.rocket_rect.colliderect(obstacle.rect) and rand != 3:
                # crash_result = pygame.sprite.collide_rect (player.rocket_rect,obstacle.rect)
                
                screen.blit(smoke, (obstacle.rect.x-60, obstacle.rect.y))
                obstacles.pop()
                player.dino_shoot = False
                break
            
            if player.dino_rect.colliderect(obstacle.rect):
                
                if rand != 3:
                    pygame.time.delay(20) # 延遲0.02秒
                    character(False)
                else:
                    obstacles.pop()
                    flag = True

            if obstacle.rect.x < -obstacle.rect.width:
                obstacles.pop()

                
            
        pygame.display.update()
        
        clock.tick(45)
        
def home():
    global width;   global height;  global case
    bgd = pygame.image.load("./picture/day.png")
    cha = pygame.image.load("./picture/msh.png")
    arrow = pygame.image.load("./picture/arrow.png") 
    
    clock = pygame.time.Clock()
    
    pos = [(480,250),(500,220),(520,250),(500,220),(480,250)]

    cnt = 0
    
    run = True
    while run:
        clock.tick(5)
        screen.blit(bgd, [0,0])
        screen.blit(cha, pos[cnt])
        cnt = (cnt+1) % 5 
        
        
        start_text2 = Text("Press enter : Start the game", 50 ,'black', (width // 2, height // 3-25))
        start_text3 = Text("Press esc : Exit the game", 50 ,'black', (width // 2, height // 3+20))
        
        start_text2.draw(screen)
        start_text3.draw(screen)
        
        
        pygame.display.flip()
  
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            
            if event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h 
                pygame.display.flip()
                
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    # print('2')
                    play(case)
                    
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    
            
def character(flag = True):
    global width;   global height
    start = [pygame.image.load("./dino/DinoStart.png") , pygame.image.load("./dino/b_DinoStart.png")]
    bgd = pygame.image.load("./picture/dessert.png") 
    arrow = pygame.image.load("./picture/arrow.png") 
    restart = pygame.image.load("./picture/Reset.png") 
    clock = pygame.time.Clock()

    run = True
    
    global case 
    
    while run:
        screen.blit(bgd, [0,0])
        
        if flag == True:
            start_text = Text("Click to choose character", 50,'black', (width // 2, height // 4) )
            x, y = pygame.mouse.get_pos()
            
            if x <= (width // 3 + 75) and x >= (width // 3 - 50):
                screen.blit(arrow, [width // 3, height // 3])
                case = 0
            if x <=(width // 2 + 75) and x >= (width // 2 - 50):
                screen.blit(arrow, [width // 2, height // 3])
                case = 1
                
            screen.blit(start[0], (width // 3, height // 2))
            screen.blit(start[1], (width // 2, height // 2))
                
        elif flag == False:
            score_text_position = (width // 2, height // 2 + 50)
            start_text = Text("Click to Restart", 40, 'BLACK', (width // 2, height // 4))
            score_text = Text("Your Score: " + str(points), 40, 'BLACK', score_text_position)
            score_text.draw(screen)
            screen.blit(restart, (width // 2 - 50, height // 3 + 20))
        
        start_text.draw(screen)
        
        clock.tick(60)
        pygame.display.update()
  
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            
            if event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h 
                pygame.display.flip()
             
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(case)
                # play(case)
                home()
                run = False
                
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    
def menu(flag = 0):
    global width;   global height
    game_speed = 0.5 # 背景移動速度
    x_pos_bg = 0    # 背景x座標
    y_pos_bg = 0  # 背景y座標
    
    bgd = pygame.image.load("./picture/dessert.png")    
    pic = pygame.image.load("./picture/menu.gif")

    
    if flag == 0:
        pygame.mixer.music.load("menu(2).mp3") 
        
        pygame.mixer.music.play(-1, 0) 
        
    run = True
    while  run:
        # background move
        image_width = bgd.get_width()
        screen.blit(bgd, (x_pos_bg, y_pos_bg))
        screen.blit(bgd, (image_width + x_pos_bg, y_pos_bg))
        x_pos_bg -= game_speed  # 使背景移動
        if x_pos_bg <= -image_width:
            screen.blit(bgd, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
            
        # menu word and picture
        death_text_position = (width // 3, height // 2)  
        dino_position = (width // 2 + 15, height // 2 - 140) 
        start_text = Text("Click to Start", 50,'black', death_text_position)
        start_text.draw(screen)
        screen.blit(pic, dino_position)
        
        pygame.display.update()
        
        for event in pygame.event.get():
        
            if event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h 
                pygame.display.flip()
                menu(1)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    character()


if __name__ == "__main__":
    
    pygame.init() 
    pygame.mixer.init() # 設置窗口大小 
    
    screenIcon = pygame.image.load('./picture/menu.gif')
    pygame.display.set_icon(screenIcon)
    
    screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)  
    pygame.display.set_caption("Adventure Of Dinosaur") 
    my_font = pygame.font.SysFont("Times New Roman", 20) 
    
    menu()
    # play()
    