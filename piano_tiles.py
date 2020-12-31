import pygame, os, random
from pygame.locals import *

wix = 450
wiy = 750

# Initializing pygame
pygame.init()

# Loading Music file here and playing
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)       # frequency variation and (-1) means that it will runs repeatedly

crash_sound = pygame.mixer.Sound("Tile_smash.wav")

def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

# Displaying of message
# Will be called outside the loop of the function "msg"
def msg(screen, text, color=(55, 55, 55), size=36, pos=(-1, -1)):
    if pos[0] == -1:
        pos = (screen.get_rect().centerx, pos[1])
    if pos[1] == -1:
        pos = (pos[0], screen.get_rect().centery)
    font = pygame.font.Font(None, size)
    text = font.render(text, 1, color)
    textpos = text.get_rect()
    textpos.centerx = pos[0]
    textpos.centery = pos[1]
    screen.blit(text, textpos)


# Button function
class Button():
    x = 0  # x, y positions
    y = -wiy // 5
    h = wix // 4 - 1
    l = wiy // 5
    enclick = True

# Position of tiles
    def pos(self, n):
        self.x = n * wix // 4

# Update of screen
    def update(self, screen):
        if self.enclick:
            pygame.draw.rect(screen, (0, 0, 0), [self.x, self.y, self.h, self.l])  # tiles are drawn here in black color
        else:
            pygame.draw.rect(screen, (180, 180, 180), [self.x, self.y, self.h, self.l])  # if false change color of tile

# Click function checks the alignment of tiles and sets the click to false
    def click(self, ps):
        if ps[0] in range(self.x, self.x + self.h):
            if ps[1] in range(self.y, self.y + self.l):
                self.enclick = False
                return 0
        return 1

# Display of title of the game
pygame.display.set_caption("~~Piano~~Tiles~~")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((wix, wiy))
lst = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 1, 2, 3, 1, 0, 2, 3, 1, 0, 1, 2,
       3]  # arrangement of tiles by order of columns defined as indexes
lost = 0    # lost is initialized to zero

time = 0
delt = 60       # delete the tiles
smallTiles = []  # array of small tiles
speed = 4       # speed of tiles on y-axis
score = 0
while lost == 0:
    for i in lst:
        smallTiles.append(Button())     # When we click on a tile it is added to small tiles
        smallTiles[-1].pos(i)
        if lost != 0:
            break
        for j in range(wiy // (5 * speed)):     #
            # print(time ,":time",delt,": delt")
            time += 1 / delt        #
            clock.tick(delt)
            screen.fill((224, 224, 255))
            if lost != 0:           # condition for lost
                break
            for k in range(len(smallTiles)):
                try:
                    smallTiles[k].y += speed  # speed of tiles increase when the game goes ahead 
                    smallTiles[k].update(screen)    # so the screen also gets updated
                    if smallTiles[k].y > wiy - smallTiles[k].l and smallTiles[k].enclick == True:
                        lost = 1
                except:
                    pass
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    lost = smallTiles[score].click(pygame.mouse.get_pos())
                    score += 1          # When you click a tile score gets increased i.e. its gets updated
            msg(screen, "SCORE " + str(score), color=(0, 128, 255), pos=(-1, 30))
            pygame.display.update()
    speed += 1
    crash()
    
msg(screen, "Game Over!", color=(110, 118, 225), pos=(-1, -1))
msg(screen, "SCORE = " + str(score), color=(0, 55, 55), pos=(-1, 70))       # When the game ends it displays the score
pygame.mixer.music.stop()   # When the game is over the music stops
pygame.display.update()
pygame.time.wait(2500)      # Screen wait time after the game is over
pygame.quit()               # Quit the game after the wait time ends
quit()
