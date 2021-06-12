import pygame,sys,os,pycountry
from abc import ABC,abstractmethod
from globe import Globe
import time
import random
pygame.init()


clock = pygame.time.Clock()
FPS = 60
WHITE = (255,) * 3
BLACK = (0,) * 3
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BGCOLOR = (64,224,208)
ORANGE = (242,133,0)
CORAL = (255,127,80)
TIMER = pygame.USEREVENT + 10

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
        gap = 40
        globe = Globe(self.screen_width//2,self.title_text_rect.bottom + gap * 2,size,rows,cols,width,height,os.path.join('images','globe.png'))
        self.globe = pygame.sprite.GroupSingle(globe)

        top = globe.rect.bottom + gap 
        self.buttons = pygame.sprite.Group()
        labels = ('COUNTRY ' + u"\u2192" + " CAPITAL" ,'CAPITAL ' + u"\u2192" + ' COUNTRY','FLAG ' + u"\u2192" + ' COUNTRY','BORDER ' + u"\u2192" +" COUNTRY")
        button_width = 400


        button_height = 75
        button_font = pygame.font.SysFont("calibri",40)
        pygame.mixer.music.load('mainmenu.ogg')


        for i in range(len(labels)):
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
        elif number == 1:
            mode = CapitalToCountry
        elif number == 2:
            mode = FlagToCountry
        else:
            mode = BorderToCountry


        
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
                        result = mode(self.screen).play()
                        pygame.mixer.music.load('mainmenu.ogg')
                        pygame.mixer.music.play(-1)
                        print(result)
                        if result == 'menu':
                            return









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
    small_font = pygame.font.SysFont("calibri",75,bold=True)
    heart_image = pygame.transform.scale(pygame.image.load(os.path.join('images','heart.png')),(50,50))
    correct_sound = pygame.mixer.Sound('positive.wav')
    incorrect_sound = pygame.mixer.Sound('negative.wav')
    buzzer_sound = pygame.mixer.Sound("buzzer.ogg")
    win_sound = pygame.mixer.Sound("win.mp3")
    def __init__(self,screen,lives=3):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        pygame.mixer.music.load("music.ogg")
        self.correct_text = self.font.render("CORRECT!",True,GREEN)
        self.incorrect_text = self.font.render("INCORRECT!",True,RED)
        self.game_over_text = self.font.render("GAME OVER",True,RED)
        self.correct = 0
        self.score_text = self.font.render("0",True,BLACK)
        self.game_over_rect = self.game_over_text.get_rect(center=(self.screen_width//2,self.screen_height//2))
        self.win_text = self.font.render("YOU WIN!",True,GREEN)
        self.win_text_rect = self.win_text.get_rect(center=(self.screen_width//2,self.screen_height//2))
        self.seconds = 0
        self.seconds_text = self.font.render(str(self.seconds),True,BLACK)
        self.streak = 0


        
        button_width = 500
        button_height = 100
        gap = 50
        play_again_button = Button(self.screen_width//2 -button_width//2,self.screen_height//4 - button_height//2,"PLAY AGAIN",BLACK,self.font,CORAL,button_width,button_height)
        menu_button = Button(self.screen_width//2 -button_width//2,self.screen_height//2 + self.screen_height//4 - button_height//2,"MENU",BLACK,self.font,CORAL,button_width,button_height)
        self.buttons = pygame.sprite.Group(play_again_button,menu_button)
        self.game_over = False
        self.result_text_2 = None
        self.lives = lives


        #self._setup()
        #self._read_data()

    

    def _check_win(self):
        if not self.countries:
            pygame.mixer.music.stop()
            self.win_sound.play()
            self.game_over = True
            self.ending_text,self.ending_text_rect = self.win_text,self.win_text_rect


    def _draw_lives(self):

        gap = 10
        for i in range(1,self.lives + 1):
            self.screen.blit(self.heart_image,(self.screen_width  - i * (gap + self.heart_image.get_width()),0))






    def  _update_answer_based_on_key_pressed(self,user_answer,key):

        

        if key == pygame.K_BACKSPACE:
            if user_answer: 
                last = user_answer[-1]
                if last == '|':
                    user_answer = user_answer[:-2] + '|'
                else:
                    user_answer = user_answer[:-1]
        else:
            key = chr(key).upper()

            if user_answer:
                last = user_answer[-1]

                if last == '|':
                    user_answer = user_answer[:-1] + key + '|'
                else:
                    user_answer += key
            else:
                user_answer += key


        return user_answer 





    

    def _get_flicker_answer(self):

        actual_user_answer = self.user_answer if self.user_answer and self.user_answer[-1] == '|' else self.user_answer + '|'
        user_answer_text = self.font.render(self.user_answer,True,BLACK)
        actual_answer_text = self.font.render(actual_user_answer,True,BLACK)
        bottom_gap = 50
        user_answer_rect = actual_answer_text.get_rect(center=(self.screen_width//2,self.screen_height - bottom_gap -  actual_answer_text.get_height()//2))

        return user_answer_text,user_answer_rect




    
    

    def _check_user_answer(self):
        
        self.user_answer = self.user_answer if self.user_answer[-1] != '|' else self.user_answer[:-1]
        if self.user_answer != self.answer:
            self.incorrect_sound.play()
            self.result_text = self.incorrect_text
            self.result_text_rect = self.incorrect_text_rect
            self.result_text_2 = self.font.render(self.answer,True,RED)
            if self.result_text_2.get_width() > self.screen_width:
                self.result_text_2 = self.small_font.render(self.answer,True,RED)

            self.result_text_2_rect = self.result_text_2.get_rect(center=(self.screen_width//2,self.question_text_rect.bottom + 50 + self.result_text_2.get_height()//2))
            self.streak = 0

            self.lives -= 1
        else:
            self.correct_sound.play()
            self.correct += 1
            self.score_text = self.font.render(str(self.correct),True,BLACK)

            self.streak += 1
            if self.streak == 10:
                self.lives = min(self.lives +1 ,3)
            self.result_text_rect = self.correct_text_rect
            self.result_text = self.correct_text
            self.result_text_2 = None
            self._check_win()

    
    def _reset(self):
        self.countries = self.original.copy()
        random.shuffle(self.countries)
        self.game_over = False
        self.streak = 0
        self.correct = 0
        self.score_text = self.font.render(str(self.correct),True,BLACK)

        self.seconds = 0
        self.seconds_text = self.font.render(str(self.seconds),True,BLACK)

        self.lives = 3
        pygame.mixer.music.load("music.ogg")
        pygame.mixer.music.play(-1)

        return self.new_question()



    def initial_timer(self):



        TIMER = pygame.USEREVENT + 5
        pygame.time.set_timer(TIMER,1000)
        
        texts = [self.font.render("READY!",True,RED),self.font.render("SET!",True,YELLOW),self.font.render("GO!",True,GREEN)]
        index = 0
        text_rect = texts[0].get_rect(center=(self.screen_width//2,self.screen_height//2))
        
        timer_sound = pygame.mixer.Sound('racestart.wav')
        
        timer_sound.play()
            
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == TIMER:
                    index += 1
                    if index == len(texts):
                        pygame.time.set_timer(TIMER,0)
                        return
                    text_rect = texts[index].get_rect(center=(self.screen_width//2,self.screen_height//2))



            self.screen.fill(BGCOLOR)

            

            self.screen.blit(texts[index],text_rect)
            pygame.display.update()



            



    
    def play(self):


        self.user_answer = '|'
        
        self.result_text = None

        bottom_gap = 50
        user_answer_text = self.font.render(self.user_answer,True,BLACK)
        user_answer_rect = user_answer_text.get_rect(center=(self.screen_width//2,self.screen_height - bottom_gap -  user_answer_text.get_height()//2))

        FLICKER_EVENT = pygame.USEREVENT + 1
        milliseconds = 300
        pygame.time.set_timer(FLICKER_EVENT,milliseconds)
        last_back_space_start = None
        result_start_time = None
        seconds = 5
        
        times_up_text = self.font.render("TIMES UP!",True,RED)
        times_up_text_rect = times_up_text.get_rect(center=self.correct_text_rect.center)
        seconds_text = self.font.render(str(seconds),True,BLACK)
        seconds_text_rect = seconds_text.get_rect(center=self.correct_text_rect.center)
        self.initial_timer()
        pygame.mixer.music.play(-1)
        pygame.time.set_timer(TIMER,1000)

        while True:

            current_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    point = pygame.mouse.get_pos()
                    if BACK_IMAGE_RECT.collidepoint(point):
                        return 
                    if self.game_over:
                        broke = False
                        for i,button in enumerate(self.buttons):
                            if button.clicked_on(point):
                                if i == 1:
                                    return "menu"
                                user_answer_text,user_answer_rect = self._reset()
                                break
                            else:
                                continue

                            break


                    
                elif not self.game_over and not result_start_time and event.type == pygame.KEYDOWN:
                    if self.user_answer not in ('|','') and event.key == pygame.K_RETURN:
                        self._check_user_answer()
                        result_start_time = time.time()
                    elif pygame.K_a <= event.key <= pygame.K_z or (self.user_answer not in ('','|') and event.key == pygame.K_SPACE) or (event.key == pygame.K_MINUS):
                        self.user_answer = self._update_answer_based_on_key_pressed(self.user_answer,event.key)
                        user_answer_text,user_answer_rect = self._get_flicker_answer()

                elif not result_start_time and not self.game_over and event.type == FLICKER_EVENT:
                    
                    if self.user_answer:
                        last = self.user_answer[-1]
                        if last == '|':
                            self.user_answer = self.user_answer[:-1]
                        else:
                            self.user_answer += '|'
                    else:
                        self.user_answer = '|'
                    

                    user_answer_text,user_answer_rect = self._get_flicker_answer()
                elif event.type == TIMER:
                    if not result_start_time:
                        seconds -= 1
                        if seconds == 0:
                            self.buzzer_sound.play()
                            self.lives -= 1
                            self.result_text= times_up_text
                            self.result_text_rect = times_up_text_rect
                            self.result_text_2 = self.font.render(self.answer,True,RED)
                            self.result_text_2_rect = self.result_text_2.get_rect(center=(self.screen_width//2,self.question_text_rect.bottom + 50 + self.result_text_2.get_height()//2))
                            result_start_time = time.time()
                            pygame.time.set_timer(TIMER,0)
                        elif seconds > 0:
                            seconds_text = self.font.render(str(seconds),True,BLACK)
                    self.seconds += 1
                    self.seconds_text = self.font.render(str(self.seconds),True,BLACK)



        
            self.screen.fill(BGCOLOR)
            self.screen.blit(BACK_IMAGE,BACK_IMAGE_RECT)

            if not self.game_over:
                if result_start_time: 
                    if current_time - result_start_time >= 2:
                        if self.lives == 0:
                            pygame.mixer.music.load("Retro_No hope.ogg")
                            pygame.mixer.music.play()
                            self.ending_text = self.game_over_text
                            self.ending_text_rect = self.game_over_rect
                            self.game_over = True
                        else:
                            user_answer_text,user_answer_rect = self.new_question()
                            seconds = 5
                            seconds_text = self.font.render(str(seconds),True,BLACK)
                            result_start_time = None
                            pygame.time.set_timer(TIMER,1000)


                keys_pressed = pygame.key.get_pressed()


                if keys_pressed[pygame.K_BACKSPACE]:
                    if last_back_space_start:
                        current_time = time.time()
                        if current_time - last_back_space_start >= 0.10:
                            self.user_answer = self._update_answer_based_on_key_pressed(self.user_answer,pygame.K_BACKSPACE)
                            user_answer_text,user_answer_rect = self._get_flicker_answer()
                            last_back_space_start = time.time()
                    else:
                        self.user_answer = self._update_answer_based_on_key_pressed(self.user_answer,pygame.K_BACKSPACE)
                        user_answer_text,user_answer_rect = self._get_flicker_answer()
                        last_back_space_start = time.time()
                elif last_back_space_start:
                    last_back_space_start = None






                

                self.screen.blit(self.header_text,self.header_text_rect)
                self.screen.blit(self.question_text,self.question_text_rect)
                self.screen.blit(user_answer_text,user_answer_rect)
                if not result_start_time:
                    self.screen.blit(seconds_text,seconds_text_rect)
                else:
                    self.screen.blit(self.result_text,self.result_text_rect)
                    if self.result_text_2:
                        self.screen.blit(self.result_text_2,self.result_text_2_rect)

                self._draw_lives()
                self.screen.blit(self.seconds_text,(0,self.screen_height - self.seconds_text.get_height()))
                self.screen.blit(self.score_text,(self.screen_width - self.score_text.get_width(),self.screen_height - self.seconds_text.get_height()))
            else:
                point = pygame.mouse.get_pos()
                self.buttons.update(point)
                self.buttons.draw(self.screen)
                self.screen.blit(self.ending_text,self.ending_text_rect)

            pygame.display.update()
            clock.tick(FPS)

        
    @abstractmethod
    def new_question(self):
        self.user_answer = '|'
        user_answer_text = self.font.render(self.user_answer,True,BLACK)
        bottom_gap = 50
        user_answer_rect = user_answer_text.get_rect(center=(self.screen_width//2,self.screen_height - bottom_gap -  user_answer_text.get_height()//2))
        return user_answer_text,user_answer_rect

    
    def _update_high_score_if_needed(self):
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
    high_score_file_name = "country_to_capital_high.txt"

    header_text= Game.font.render("CAPITAL OF",True, BLACK)
    Game.font.set_underline(False)
    def __init__(self,screen):
        super().__init__(screen)
        
        self._read_data()

        self._setup()

    

    def _update_high_score_if_needed(self):


        if self.score > self.high_scores[-1]:
            self.high_scores.pop()
            self.high_scores.append(self.score)
            self.high_scores.sort()

            with open(self.high_score_file_name,'w') as f:
                for score in self.high_scores:
                    f.write(str(score) + '\n')




    def new_question(self):
        if isinstance(self,CapitalToCountry):
            return super().new_question()
        question,self.answer = self.countries.pop()
        self.answer = self.answer.strip()
        self.question_text = self.font.render(question + "?",True,BLACK)

        self.question_text_rect = self.question_text.get_rect(center=(self.screen_width//2,self.screen_height//2))


        return super().new_question()



    
    def _setup(self):


        self.header_text_rect= self.header_text.get_rect(center=(self.screen_width//2,50 + self.header_text.get_height()//2))
        self.correct_text_rect = self.correct_text.get_rect(center=(self.screen_width//2,self.header_text_rect.bottom + 50 + self.correct_text.get_height()//2))
        self.incorrect_text_rect = self.incorrect_text.get_rect(center=(self.screen_width//2,self.header_text_rect.bottom + 50 + self.incorrect_text.get_height()//2))
        self.new_question()






    def _read_data(self):


        with open(self.high_score_file_name,'r') as f:
            self.high_scores = list(map(int,f.readlines()))



        self.countries = []
        with open(self.file_name,'r') as f:
            for i,line in enumerate(f):
                if i == 0:
                    continue
                country,capital = line.split(',')
                self.countries.append((country.upper(),capital.upper()))
        
        self.original = self.countries.copy()
        random.shuffle(self.countries)

class CapitalToCountry(CountryToCapital):
    Game.font.set_underline(True)
    header_text= Game.font.render("COUNTRY OF",True, BLACK)
    Game.font.set_underline(False)




    def new_question(self):
        self.answer,question= self.countries.pop()
        self.answer = self.answer.strip()
        question = question.strip()
        self.question_text = self.font.render(question + "?",True,BLACK)

        self.question_text_rect = self.question_text.get_rect(center=(self.screen_width//2,self.screen_height//2))


        return super().new_question()



class FlagToCountry(Game):
    

    dir_name = 'flag_images'
    Game.font.set_underline(True)
    header_text = Game.font.render("COUNTRY OF",True,BLACK)
    Game.font.set_underline(False)
    def __init__(self,screen):
        super().__init__(screen)
        
        self._read_data()

        self._setup()
    



    def _read_data(self):
        image_files = os.listdir(self.dir_name)

        
        
        self.countries = [image_file for image_file in image_files if not image_file.startswith('.')]
        self.original = self.countries.copy()


        random.shuffle(self.countries)

        



    
    def _setup(self):
        self.header_text_rect= self.header_text.get_rect(center=(self.screen_width//2,50 + self.header_text.get_height()//2))
        self.correct_text_rect = self.correct_text.get_rect(center=(self.screen_width//2,self.header_text_rect.bottom + 50 + self.correct_text.get_height()//2))
        self.incorrect_text_rect = self.incorrect_text.get_rect(center=(self.screen_width//2,self.header_text_rect.bottom + 50 + self.incorrect_text.get_height()//2))
        self.new_question()

    def new_question(self):
        
        if isinstance(self,BorderToCountry):
            return super().new_question()
        
        image_name = self.countries.pop()

        self.answer,_ = image_name.split('.')


        self.answer = self.answer.upper().replace('_',' ')





        self.question_text = pygame.image.load(os.path.join(self.dir_name,image_name)).convert_alpha()
        width,height = self.question_text.get_size()
        ratio = width/height

        new_height = 220
        new_width = int(new_height * ratio)
        print(new_height,new_width)


        self.question_text = pygame.transform.scale(self.question_text,(new_width,new_height))


        self.question_text_rect = self.question_text.get_rect(center=(self.screen_width//2,self.screen_height//2))


        return super().new_question()

class BorderToCountry(FlagToCountry):

    dir_name = 'country_images'


    def new_question(self):

        image_name = self.countries.pop()

        code,_ = image_name.split('.')


        self.answer = pycountry.subdivisions.get(code=f"US-{code}").name.upper()


        self.question_text = pygame.image.load(os.path.join(self.dir_name,image_name)).convert_alpha()
        width,height = self.question_text.get_size()
        ratio = width/height

        new_height = 220
        new_width = int(new_height * ratio)


        self.question_text = pygame.transform.scale(self.question_text,(new_width,new_height))


        self.question_text_rect = self.question_text.get_rect(center=(self.screen_width//2,self.screen_height//2))


        return super().new_question()





if __name__ == "__main__":
    
    SCREEN_WIDTH = 1500
    SCREEN_HEIGHT = 800
    Menu(SCREEN_WIDTH,SCREEN_HEIGHT)


