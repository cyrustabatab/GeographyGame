import pygame,os




class Spritesheet:


    def __init__(self,filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except Exception as e:
            print(e)
            print("Unable to read spritesheet")


    def image_at(self,rectangle,colorkey=None,size=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size,pygame.SRCALPHA)
        image.blit(self.sheet,(0,0),rect)
        if size is not None:
            image = pygame.transform.scale(image,(size,size))
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey,pygame.RLEACCEL)
        return image


    def images_at(self,rects,colorkey=None,size=None):

        return [self.image_at(rect,colorkey,size) for rect in rects]


    def load_strip(self,rect,image_count,colorkey=None,size=None):

        rects = [(rect[0] + rect[2] * x,rect[1],rect[2],rect[3]) for x in range(image_count)]

        return self.images_at(rects,colorkey,size)







