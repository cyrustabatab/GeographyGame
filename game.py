import pygame,sys,os
from globe import Globe
pygame.init()


WHITE = (255,) * 3
BLACK = (0,) * 3
RED = (255,0,0)

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







class Menu:

    background = pygame.image.load(os.path.join('images','world_map.jpg'))
    font = pygame.font.SysFont("calibri",80,bold=True)





    def __init__(self,screen_width,screen_height):
        self.screen = pygame.display.set_mode((screen_width,screen_height))
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
            

            point = pygame.mouse.get_pos()


            self.buttons.update(point)



            self.screen.blit(self.background,(0,0))
            self.screen.blit(self.title_text,self.title_text_rect)
            self.buttons.draw(self.screen)
            self.globe.draw(self.screen)
            pygame.display.update()
        




if __name__ == "__main__":
    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    Menu(SCREEN_WIDTH,SCREEN_HEIGHT)


