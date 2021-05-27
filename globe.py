from spritesheet import Spritesheet
import pygame




class Globe(pygame.sprite.Sprite):


    def __init__(self,x,y,size,rows,cols,width,height,filename):
        super().__init__()
        "rows is number of rows in spritesheet for globe, col is numbre oc olumns, width is width of image"
        # x and y represent center of globe image

        self.images = self._load_images(filename,rows,cols,width,height,size)

        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(x,y))
        self.image_index = 0

    def update(self):

        self.image_index = (self.image_index + 1) % len(self.images)

        self.image = self.images[self.image_index]



        
    def _load_images(self,filename,rows,cols,width,height,size):
        spritesheet = Spritesheet(filename)

        images = []
        for row in range(rows):
            images.extend(spritesheet.load_strip((0,height * row,width,height),cols,size=size))
        
        return images
    













