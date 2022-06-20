import pygame # cmd(명령 프롬프트 창)에서 "pip install pygame" 를 입력하여 pygame모듈을 다운받을 수 있습니다.
import random
import math


pygame.init()

clock = pygame.time.Clock()

#색 설정
black = (0,0,0)
white =  (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
lightblue = (0,155,155)

#창 크기 설정
info_object = pygame.display.Info()
window_width, window_height = info_object.current_w, info_object.current_h
display_surface = pygame.display.set_mode((info_object.current_w, info_object.current_h))
pygame.display.set_caption("지훈이의 피하기 게임")

#텍스트 클래스 설정
class Text:
    def __init__(self, text, size, tcolor, x, y, show):
        font = pygame.font.Font("Pro.ttf", size)
        self.font = font.render(text, True, tcolor)
        self.rect = self.font.get_rect()
        self.rect.midtop = (x,y)
        if show:
            display_surface.blit(self.font, self.rect)

#플레이어 클래스 설정
class Player:
    def __init__(self, address, x,y):
        self.image = pygame.image.load(address)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x,y

    def change_size(self, sx, sy):
        x,y = self.rect.centerx, self.rect.centery
        self.image = pygame.transform.scale(self.image, (sx, sy))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x,y
    
    def shift(self,x,y):
        self.rect.centerx, self.rect.centery = x,y
    
    def disappear(self):
        pass

class Bomb(Player):
    def __init__(self, address, x, y):
        super().__init__(address, x, y)
        self.speedx, self.speedy, self.directx, self.directy = 1,1,1,1
    def disappear(self):
        bombs.remove(self)
        bomb1 = Bomb(".\\images\\bomb.png", window_width, random.randint(0, window_height))
        bomb1.directx, bomb1.directy = -1, 1
        bombs.append(bomb1)
        bomb1.change_size(120,120)

class Carrot(Player):
    def __init__(self, address, x, y):
        super().__init__(address, x, y)
        self.__speed =3
        self.direct = random.randint(0,4)
        if self.direct == 0:
            self.shift(random.randint(60,window_width-60), 0)
        elif self.direct == 1:
            self.shift(random.randint(60,window_width-60), window_height)
        elif self.direct == 2:
            self.shift(0, random.randint(60,window_height-60))
        elif self.direct == 3:
            self.shift(window_width, random.randint(60,window_height-60))
        
    def move(self):
        if self.direct == 0:
            self.rect.y += self.__speed
        elif self.direct == 1:
            self.rect.y -= self.__speed
        elif self.direct == 2:
            self.rect.x += self.__speed
        elif self.direct == 3:
            self.rect.x -= self.__speed
        
    def disappear(self):
        carrots.remove(self)

#이미지 정의하기
running_bunny = Player(".\\images\\runningbunny.png", (window_width//2), 0)
running_bunny.change_size(80,100)

#아이템 리스트 설정
bombs = []
carrots = []

#시작 화면
def start_screen():
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                global running
                running = False
                
            if event.type == pygame.KEYUP:
                waiting = False
        
        #창 덮기
        display_surface.fill(lightblue)
        
        #문구 채우기
        title = Text("피해봐요, 할 수 있으면...", 32, black, window_width//2, 80, 1)
        explanation = Text("사용방법 : 방향키 또는 wasd로 날아오는 물체들을 피하고 당근을 획득하세요!", 18, black, window_width//2, 120, 1)
        state = Text("아무 키나 눌러서 시작하세요", 18, black, window_width//2, 500, 0)
        if (pygame.time.get_ticks()//500)%2:
            display_surface.blit(state.font, state.rect)
        
        pygame.display.update()
        clock.tick(60)
    
    return

#인트로 화면
def intro_screen():
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                intro = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            running_bunny.shift(window_width//2, window_height//2)
            intro = False

        display_surface.fill(black)

        if running_bunny.rect.y == window_height//2:
            intro = False
        running_bunny.rect.y += 2
        
        display_surface.blit(running_bunny.image, running_bunny.rect)
        intro_title = Text("하늘에서 내려온 토끼에게 당근을 선물해봐요!", 32, lightblue, window_width//2, 80, 1)
        intro_exp1 = Text("당근을 먹으면 점수가 올라가고 물체에 닿으면 목숨이 사라집니다.", 20, lightblue, window_width//2, 130,1)
        intro_exp2 = Text("좋은 아이템도 있을거에요 아마?", 20, lightblue, window_width//2, 150, 1)
        intro_exp3 = Text("spacebar를 누르면 이 화면을 넘길 수 있어요", 20, lightblue, window_width//2, 170, 1)
        pygame.display.update()

        clock.tick(60)
    if running:
        pygame.time.delay(500)

        display_surface.fill(white)
        start_state = Text("시작!", 40, black, window_width//2, window_height//2, 1)
        pygame.display.update()
        clock.tick(60)
        pygame.time.delay(1000)

    return

#엔드 화면    
def end_screen(score):
    end = True

    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                end = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            end = False
            running = False
            break
        
        if keys[pygame.K_SPACE]:
            end = False
        
        display_surface.fill(black)
        end_mes1 = Text("당신의 점수는 "+str(score)+" 입니다.", 30, white, window_width//2, 150, 1)
        end_mes2 = Text("다시 플레이 하고 싶으시다면 spacebar를, 종료하고 싶으시다면 esc를 눌러주세요.", 20, white, window_width//2, 300, 1)
        pygame.display.update()
        clock.tick(60)
    
    return

running = True
if running :
    start_screen()
if running:
    intro_screen()
start_time = int(pygame.time.get_ticks())

life = 15
score = 0
c_count = 0
b_count = 0
skill = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #key값 리스트로 입력받기
    keys = pygame.key.get_pressed()

    #토끼 움직이기
    bunny_speed = 12
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and running_bunny.rect.left > 0:
        running_bunny.rect.x -= bunny_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and running_bunny.rect.right < window_width:
        running_bunny.rect.x += bunny_speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and running_bunny.rect.top >0:
        running_bunny.rect.y -= bunny_speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and running_bunny.rect.bottom < window_height:
        running_bunny.rect.y += bunny_speed

    #게임 진행 시간
    game_time = pygame.time.get_ticks() - start_time

    #폭탄 추가하기
    if game_time//10000 +1 > b_count:
        bomb1 = Bomb(".\\images\\bomb.png", 0, random.randint(0,window_height))
        b_count += 1
        bomb1.change_size(120,120)
        bombs.append(bomb1)

    #폭탄 자동 움직임
    for bomb in bombs:
        bomb.speedx = 3+(game_time)//5000
        bomb.speedy = 3+(game_time)//5000

        if bomb.rect.x > (window_width + 150) or bomb.rect.x < -150:
            bomb.directx *= -1
        if bomb.rect.y > (window_height + 150) or bomb.rect.y < -150:
            bomb.directy *= -1

        bomb.rect.x += bomb.speedx*bomb.directx
        bomb.rect.y += bomb.speedy*bomb.directy    

        if bomb.rect.colliderect(running_bunny.rect):
            life -=1
            bomb.disappear()
    
    #당근 추가하기
    if game_time//1000 + 1 > c_count:
        carrot1 = Carrot(".\\images\\normalcarrot.png", window_width+100, window_height+100)
        carrot1.change_size(120,120)
        c_count += 1
        carrots.append(carrot1)
    
    #당근 자동 움직임
    for carrot in carrots:
        if carrot.rect.x < -200 or carrot.rect.x > window_width+200:
            carrot.disappear()
        if carrot.rect.y < -200 or carrot.rect.y > window_height+200:
            carrot.disappear()
        
        carrot.move()

        

        if carrot.rect.colliderect(running_bunny.rect):
            score += 1
            carrot.disappear()

    #창 덮기
    display_surface.fill(white)

    #플레이어 나타내기
    display_surface.blit(running_bunny.image, running_bunny.rect)
    for bomb in bombs:
        display_surface.blit(bomb.image, bomb.rect)
    for carrot in carrots:
        display_surface.blit(carrot.image, carrot.rect)

    
    #텍스트 나타내기
    life_board = Text("life : " + str(life), 30, black, 50, 0, 0)
    life_board.rect.topleft = (0,0)
    display_surface.blit(life_board.font, life_board.rect)
    score_board = Text("score : "+str(score), 30, black, 70, 25, 0)
    score_board.rect.topleft = (0,25)
    display_surface.blit(score_board.font, score_board.rect)

    if life == 0:
        end_screen(score)   
        life = 15
        score = 0
        start_time = int(pygame.time.get_ticks())
        bombs = []
        carrots = []
        skill_points = []
        b_count = 0
        c_count = 0
    
    #디스플레이 업데이트
    pygame.display.update()

    #fps 설정
    clock.tick(60)

pygame.quit()