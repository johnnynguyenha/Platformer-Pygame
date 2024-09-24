from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        # self.load_images()
        # self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load(join('images', 'player', '0.png')).convert_alpha()
        self.pos = pos
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect
        self.frame_index = 0
        self.animation_speed = 6
        self.frames = []
        self.old_rect= self.rect.copy()
        self.facing_right = True
        self.can_jump = 1

        # movement
        self.velocity = 300
        self.direction = pygame.math.Vector2(0,0)
        self.collision_sprites = collision_sprites

        self.load_images()

    def load_images(self):   
        for _, _, file_names in walk(join('images', 'player')):
            # Sort filenames to ensure frames are loaded in the correct order
            for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                full_path = join('images', 'player', file_name)
                surf = pygame.image.load(full_path).convert_alpha()  # Load image with alpha channel
                self.frames.append(surf)
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        if int(keys[pygame.K_SPACE]) == 1 and self.can_jump == 1:
            self.direction.y = -1
            self.can_jump = 0
        self.direction = self.direction.normalize() if self.direction else self.direction # no matter what direction, will always be at the same speed
    def move(self, dt):
        self.rect.x += self.direction.x * self.velocity * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.velocity * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
         for sprite in self.collision_sprites:
             if sprite.rect.colliderect(self.hitbox_rect):
                 if direction == 'horizontal':
                     if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left # if the player is moving right (direction x > 0), then put the player's right side on the left of the collided object
                     if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                 if direction == 'vertical':
                     if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                     if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
    def animate(self, dt):
        if self.direction.x == 0:
            if not self.facing_right:
                self.frame_index = 0
                self.image = pygame.transform.flip(self.frames[int(self.frame_index) % len(self.frames)], True, False)
            else:
                self.frame_index = 0
                self.image = self.frames[int(self.frame_index) % len(self.frames)]
        if self.direction.x > 0:
            self.frame_index += self.animation_speed * dt
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
            self.facing_right = True
            
        if self.direction.x < 0:
            self.frame_index += self.animation_speed * dt
            self.image = pygame.transform.flip(self.frames[int(self.frame_index) % len(self.frames)], True, False)
            self.facing_right = False

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.animate(dt)
