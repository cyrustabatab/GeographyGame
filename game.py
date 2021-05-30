import pygame,sys,os
from abc import ABC,abstractmethod
from globe import Globe
import random
pygame.init()

WHITE = (255,) * 3
BLACK = (0,) * 3
RED = (255,0,0)
BGCOLOR = (64,224,208)
ORANGE = (242,133,0)
CORAL = (255,127,80)

class Button(pygame.sprite.Sprite):

    def __init__(self,x,y,text,text_color,text_font,button_color,button_width=None,button_height=None):
        super().__init__()

        self.original_image = pygame.Surface((button_width,button_height))
        self.original_rect = self.original_image.get_rect(topleft=(x,y))
        
        self.original_image.fill(button_color)
        text = text_font.render(text,True,text_color)

        self.original_image.blit(text,(button_width//2 - text.get_width()//2,button_height//2 - text.get_height()//2))

        self.expanded_image = pygame.Surface((button_width + 20,button_height + 20))
        self.expanded_image.fill(button_color)

        self.expanded_rect = self.expanded_image.get_rect(center=self.original_rect.center)


        self.expanded_image.blit(text,((button_width + 20)//2 - text.get_width()//2,(button_height + 20)//2 - text.get_height()//2))

        self.hovered_on = False

        self.rect = self.original_rect
        self.image = self.original_image


    def update(self,point):

        collided = self.rect.collidepoint(point)
        if not self.hovered_on and collided:
            self.rect = self.expanded_rect
            self.image = self.expanded_image
            self.hovered_on = True
        elif self.hovered_on and not collided:
            self.rect = self.original_rect
            self.image = self.original_image
            self.hovered_on = False

    
    def clicked_on(self,point):

        return self.rect.collidepoint(point)



BACK_IMAGE = BACK_IMAGE_RECT =  None

class Menu:

    background = pygame.image.load(os.path.join('images','world_map.jpg'))
    font = pygame.font.SysFont("calibri",80,bold=True)

    button_font = pygame.font.SysFont("calibri",40)



    def __init__(self,screen_width,screen_height):
        global BACK_IMAGE,BACK_IMAGE_RECT
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        BACK_IMAGE= pygame.transform.scale(pygame.image.load(os.path.join('images','back.png')).convert_alpha(),(50,50))
        BACK_IMAGE_RECT =BACK_IMAGE.get_rect(topleft=(0,0))
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.display.set_caption("GEO WHIZ")
        self.background = pygame.transform.scale(self.background,(self.screen_width,self.screen_height))
        self.title_text = self.font.render("GEO WHIZ",True,RED)
        self.title_text_rect = self.title_text.get_rect(center=(self.screen_width//2,50 + self.title_text.get_height()//2))
        rows = 8
        cols = 9
        width = height = 450
        size = 200
        gap = 50
        globe = Globe(self.screen_width//2,self.title_text_rect.bottom + gap * 2,size,rows,cols,width,height,os.path.join('images','globe.png'))
        self.globe = pygame.sprite.GroupSingle(globe)

        top = globe.rect.bottom + gap 
        self.buttons = pygame.sprite.Group()
        labels = ('COUNTRY ' + u"\u2192" + " CAPITAL" ,'CAPITAL ' + u"\u2192" + ' COUNTRY','FLAG ' + u"\u2192" + ' COUNTRY')
        button_width = 400
        button_height = 100
        button_font = pygame.font.SysFont("calibri",40)
        pygame.mixer.music.load('mainmenu.ogg')


        for i in range(3):
            button = Button(self.screen_width//2 -button_width//2,top + (button_height + gap) * i,labels[i],BLACK,button_font,RED,button_width,button_height)
            self.buttons.add(button)
        
        self._start()

    def _start(self):
        
        

        GLOBE_EVENT = pygame.USEREVENT + 2 
        milliseconds = 100
        pygame.time.set_timer(GLOBE_EVENT,milliseconds)
        pygame.mixer.music.play(-1)
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == GLOBE_EVENT:
                    self.globe.update()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    for i,button in enumerate(self.buttons):
                        if button.clicked_on(point):
                            result= self.instructions(i)
                            break


            

            point = pygame.mouse.get_pos()


            self.buttons.update(point)



            self.screen.blit(self.background,(0,0))
            self.screen.blit(self.title_text,self.title_text_rect)
            self.buttons.draw(self.screen)
            self.globe.draw(self.screen)
            pygame.display.update()
        
    def instructions(self,number):
        
        
        self.font.set_underline(True)
        title_text = self.font.render("INSTRUCTIONS",True,BLACK)
        self.font.set_underline(False)
        title_text_rect = title_text.get_rect(center=(self.screen_width//2,50 + title_text.get_height()//2))


        if number == 0:
            mode = CountryToCapital

        
        button_width = 400
        button_height = 100
        gap = 50
        button = Button(self.screen_width//2 -button_width//2,self.screen_height - gap - button_height,"START",BLACK,self.font,CORAL,button_width,button_height)
        button = pygame.sprite.GroupSingle(button)
        if number == 0:
            instructions_text = self.font.render("GUESS THE CAPITAL OF THE COUNTRY!",True,BLACK)
        elif number == 1:
            instructions_text = self.font.render("GUESS THE COUNTRY OF THE CAPITAL!",True,BLACK)
        else:
            instructions_text = self.font.render("GUESS THE COUNTRY FROM THE FLAG!",True,BLACK)
        

        instructions_text_2 = self.font.render("HAVE THREE LIVES!",True,BLACK)
        instructions_text_3 = self.font.render("GAIN A LIFE ON A STREAK OF 10 CORRECT!",True,BLACK)
        instructions_text_4 = self.font.render("TRY AND ANSWER AS MANY AS YOU CAN!",True,BLACK)


        gap = 10        
        instructions_text_rect = instructions_text.get_rect(topleft=(self.screen_width//2 - instructions_text.get_width()//2,title_text_rect.bottom + gap ))

        instructions_text_2_rect = instructions_text_2.get_rect(topleft=(self.screen_width//2 - instructions_text_2.get_width()//2,instructions_text_rect.bottom + 50))

        instructions_text_3_rect = instructions_text_3.get_rect(topleft=(self.screen_width//2 - instructions_text_3.get_width()//2,instructions_text_2_rect.bottom + 50))
        instructions_text_4_rect = instructions_text_4.get_rect(topleft=(self.screen_width//2 - instructions_text_4.get_width()//2,instructions_text_3_rect.bottom + 50))
        

        texts = [(title_text,title_text_rect),(instructions_text,instructions_text_rect),(instructions_text_2,instructions_text_2_rect),(instructions_text_3,instructions_text_3_rect),(instructions_text_4,instructions_text_4_rect)]



        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    

                    if BACK_IMAGE_RECT.collidepoint(point):
                        return "back"

                    if button.sprite.clicked_on(point):
                        mode(self.screen)
                        pygame.mixer.music.load('mainmenu.ogg')
                        pygame.mixer.music.play(-1)









            point = pygame.mouse.get_pos()

            button.update(point)
            self.screen.fill(BGCOLOR)
            for text,text_rect in texts:
                self.screen.blit(text,text_rect)
            button.draw(self.screen)
            self.screen.blit(BACK_IMAGE,BACK_IMAGE_RECT)
            pygame.display.update()

class Game(ABC):

    font = pygame.font.SysFont("calibri",100,bold=True)
    def __init__(self,screen):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        pygame.mixer.music.load("music.ogg")


    
    def play(self):

        pygame.mixer.music.play(-1)
        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    if BACK_IMAGE_RECT.collidepoint(point):
                        return 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.new_question()


            

            self.screen.fill(BGCOLOR)
            self.screen.blit(BACK_IMAGE,BACK_IMAGE_RECT)
            self.screen.blit(self.header_text,self.header_text_rect)
            self.screen.blit(self.question_text,self.question_text_rect)
            pygame.display.update()

        
        @abstractmethod
        def new_question(self):
            pass


        @abstractmethod
        def _setup(self):
            pass


        @abstractmethod
        def _read_data(self):
            pass

class CountryToCapital(Game):
    
    file_name = "countries_and_capitals.csv"
    Game.font.set_underline(True)
    header_text= Game.font.render("CAPITAL OF",True, BLACK)
    Game.font.set_underline(False)
    def __init__(self,screen):
        super().__init__(screen)
        
        self._read_data()

        self._setup()
        self.play()

    

    def new_question(self):
        question,answer = self.countries.pop()

        self.question_text = self.font.render(question + "?",True,BLACK)

        self.question_text_rect = self.question_text.get_rect(center=(self.screen_width//2,self.screen_height//2))



    
    def _setup(self):


        self.header_text_rect= self.header_text.get_rect(center=(self.screen_width//2,50 + self.header_text.get_height()//2))
        self.new_question()






    def _read_data(self):
        self.countries = []
        with open(self.file_name,'r') as f:
            for i,line in enumerate(f):
                if i == 0:
                    continue
                country,capital = line.split(',')
                self.countries.append((country.upper(),capital.upper()))
        

        random.shuffle(self.countries)



if __name__ == "__main__":
    
    SCREEN_WIDTH = 1500
    SCREEN_HEIGHT = 800
    Menu(SCREEN_WIDTH,SCREEN_HEIGHT)


