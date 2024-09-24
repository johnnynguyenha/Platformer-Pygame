from settings import * 
from pytmx.util_pygame import load_pygame
from sprites import *
from player import *
from groups import *
from random import choice, randint

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # load game
        self.setup()


    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Main').tiles(): #import ground in tiles
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in map.get_layer_by_name('Decoration').tiles(): #import decorations in tiles
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, (self.all_sprites))

        for obj in map.get_layer_by_name('Entities'): #import ground in tiles
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)



        #for obj in map.get_layer_by_name('Main'): # import objects in tiles
            #CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

       #  for collide in map.get_layer_by_name('Collisions'): # import collisions
            #CollisionSprite((collide.x, collide.y), pygame.Surface((collide.width, collide.height)), (self.collision_sprites))
 
    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.all_sprites.update(dt)

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 