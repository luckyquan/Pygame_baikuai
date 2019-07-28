import pygame
import pygame.locals as locals
import random
pygame.init()

class View(object):
    IMG = pygame.image.load("./res/beijing.png")
    def __init__(self):
        HEIGHT = int(Game.SIZE[1]/2)
        WIDTH = Game.SIZE[0]
        self.surf = pygame.Surface((WIDTH,HEIGHT))
        self.surf.fill((200,200,200))

    def draw(self,surface):#将黑块画在屏幕上
        surface.blit(View.IMG,(0,int(Game.SIZE[1]/2)))

class black_Piece(object): #创建黑块
    def __init__(self):
        HEIGHT = int(Game.SIZE[1]/4)
        WIDTH = int(Game.SIZE[0]/4)
        self.surf = pygame.Surface((WIDTH,HEIGHT))
        self.surf.fill((0,0,0))
        #self.rect = self.surf.get_rect()
        ret = random.randint(0,3)
        self.x = ret*WIDTH
        self.y = -HEIGHT
        self.alive = 0 #给黑块设置状态位，0表示黑块正常，1表示黑块死亡，2表示黑块被正确点击
        self.score = 1

    def draw(self,surface):#将黑块画在屏幕上
        surface.blit(self.surf,(self.x,self.y))

    def update(self):#更新黑块，给一个向下的速度
        self.y+=5
        if self.y>Game.SIZE[1]:
            self.alive = 2

class Black_manager(object):#管理黑块类
    def __init__(self,surface,score):#初始化一个黑块列表,传入score对象
        self.blacks = []
        self.surface = surface
        self.count = 0
        self.score = score

    def drawBlacks(self):#将黑快画在屏幕上
        for black in self.blacks:
            black.draw(self.surface)#画出黑块

    def update_black(self):
        self.create_black()
        index = len(self.blacks)-1
        while index >=0:
            black = self.blacks[index]
            if black.alive==0:
                black.update()
            elif black.alive==1:
                self.blacks.remove(black)
            index -=1
    def create_black(self):
        self.count += 1
        if self.count % 30 == 0:
            self.blacks.append(black_Piece())  # 隔一段时间生成黑块
            self.count = 0

    def knock(self,num):#判断黑块存活情况
        if len(self.blacks)>=1:
            if self.blacks[0].x!=int(Game.SIZE[0]/4) * num:
                self.blacks[0].alive = 2
            if self.blacks[0].y > Game.SIZE[1]:
                self.blacks[0].alive = 2
            elif self.blacks[0].y> int(Game.SIZE[1]/2) and self.blacks[0].x == int(Game.SIZE[0]/4) * num:
                # black.surf.fill((200,200,200))
                self.score.score+=self.blacks[0].score
                self.blacks.remove(self.blacks[0])
            elif self.blacks[0].y< int(Game.SIZE[1]/2)and self.blacks[0].x == int(Game.SIZE[0]/4) * num:
                self.blacks[0].alive = 2
        # for black in self.blacks:
        #     if black.y>Game.SIZE[1]:
        #         black.alive = 2
        #     elif black.y> int(Game.SIZE[1]/2) and black.x == int(Game.SIZE[0]/4) * num:
        #         # black.surf.fill((200,200,200))
        #         self.score.score+=black.score
        #         self.blacks.remove(black)
        #     elif black.y< int(Game.SIZE[1]/2)and black.x == int(Game.SIZE[0]/4) * num:
        #         black.alive = 2

class Game(object):
    SIZE = (360,600)
    FPS = 60
    def __init__(self):
        self.surface = pygame.display.set_mode(Game.SIZE)
        self.clock = pygame.time.Clock()
        self.game_init()
        # self.black_piece = black_Piece()


    def game_init(self):
        self.Running = True
        self.score = Score()
        self.view = View()
        self.blackmanager = Black_manager(self.surface,self.score)


    def start(self):
        while self.Running:
            self.control()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(Game.FPS)

    def control(self):
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                self.stop()
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_1:
                    self.blackmanager.knock(0)
                if event.key == locals.K_2:
                    self.blackmanager.knock(1)
                if event.key == locals.K_3:
                    self.blackmanager.knock(2)
                if event.key == locals.K_4:
                    self.blackmanager.knock(3)



    def draw(self):
        self.surface.fill((255,255,255))
        # self.black_piece.draw(self.surface)


        self.view.draw(self.surface)
        self.blackmanager.drawBlacks()
        self.score.draw(self.surface)

    def update(self):
        self.blackmanager.update_black()
        for black in self.blackmanager.blacks:
            if black.alive == 2:
                print("重新开始......")
                self.restart()
        self.score.update()


    def stop(self):
        self.Running = False

    def restart(self):
        self.game_init()

class Score(object):
    def __init__(self):
        self.score = 0
        self.all_imgs=[]
        for i in range(10):
            img = pygame.image.load("./res/"+str(i)+".png")
            self.all_imgs.append(img)
        self.x=0
        self.y=30
        self.imgs=[] #需要绘制的图片

    def draw(self,surface):
        pre_width = 0
        for img in self.imgs:
            surface.blit(img,(self.x+pre_width,self.y))
            pre_width = img.get_width()
            self.x = self.x + pre_width


    def update(self):
        self.imgs.clear()
        index = self.splitScore()
        width = 0
        for i in index:
            self.imgs.append(self.all_imgs[i])
        for img in self.imgs:
            width +=img.get_width()

        self.x=(Game.SIZE[0]-width)/2

    def splitScore(self):
        index_list = []
        score = self.score
        while True:
            ret = score % 10
            index_list.insert(0, ret)
            score = int(score/10)
            if score == 0:
                break

        return tuple(index_list)

if __name__=='__main__':
    game = Game()
    game.start()