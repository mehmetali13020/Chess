import pygame 
pygame.init()

board_len = 8
tile_size = 70
win_height = 560 
win_width = 560
window = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("deneme")
alive_pieces = []
dia_move = [(1,1),(-1,-1),(1,-1),(-1,1)]
str_move = [(1,0),(0,1),(-1,0),(0,-1)]
# grid = [[0 for i in range(board_len)]for j in range(board_len)]

class Piece:
    def __init__(self,color,location):
        self.color = color
        self.loc = location

class King(Piece):
    def __init__(self, color, location):
        super().__init__(color, location)
        # self.movement = [(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0)]
        self.movement = dia_move + str_move
    def next_move(self):
        ava_sqr = []
        x,y = self.loc
        for dx,dy in self.movement:
            ava_sqr.append((dx+x,dy+y))
        return ava_sqr

def place_pieces():
    grid = [[0 for i in range(board_len)]for j in range(board_len)]
    for i in range(board_len):
        for j in range(board_len):
            if (i+j) %2 == 0:
                grid[i][j] = "."
            else:
                grid[i][j] = "#"
    with open("locations.txt") as file:
        line = file.readline()
        kind, color, loc = line.split(", ")
        match kind:
            case "King":
                King(color,loc)
    return grid


def display_board():
    for i in range(len(board_len)):
        for j in range(board_len):
            
            if (i+j) %2 == 0:
                color = (255,255,255) 
            else:
                color = (0,0,0) 
            
            pygame.draw.rect(window, color, (j*tile_size,i*tile_size,tile_size,tile_size))


running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONUP:
            loc = pygame.mouse.get_pos()
            x,y = loc
            loc_coord = ((y//tile_size),(x//tile_size)+1)
            i,j = loc_coord
            
            if not(grid[j][i] in [".","#"]): #right here
                pass


        for i in range(board_len):
            for j in range(board_len):
                if (i + j) % 2 == 0:
                    tile = "#"
                else:
                    tile = "."
                grid[j][i] = tile

    window.fill((0, 0, 0))
    display_board()
    grid = place_pieces()
    
    




    pygame.display.update()
pygame.quit()

