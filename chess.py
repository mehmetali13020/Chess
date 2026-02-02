import pygame
from images import *
pygame.init()


#GLOBALDE BU KADAR İNFO OLMAZ GEREKENİ GEREKEN YERE KOY
turn_count = 0
board_len = 8
tile_size = 70
win_height = 560
win_width = 560
circle_radius = 10
circle_green = (89, 217, 123)
white = (255,255,255)
black = (0,0,0)
space = [".","#"]
selected_piece = None
window = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("deneme")
alive_pieces = []
dia_move = [(1,1),(-1,-1),(1,-1),(-1,1)]
str_move = [(1,0),(0,1),(-1,0),(0,-1)]
knight_move = [(2,-1),(2,1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)]
colors = ["White", "Black"]
pawn_row = {"White": 1, "Black": 6} #rows that pawns exist
other_row = {"White": 0, "Black": 7} #rows that other pieces exist
pieces_order = ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"] #piece by count
board_len = 8
pawns = 8
# grid = [[0 for i in range(board_len)]for j in range(board_len)]

class Piece:
    def __init__(self,color,location,kind,image):
        self.slow = False
        self.color = color
        self.loc = location
        self.kind = kind
        self.image = image
        if kind == "Rook":
            self.move = str_move
            self.played = False
        elif kind == "Bishop":
            self.move = dia_move
        elif kind == "Queen":
            self.move = str_move + dia_move
        elif kind == "King":
            self.move = str_move + dia_move
            self.slow = True
            self.played = False
        elif kind == "pawn":
            if self.color == "Black":
                self.move = [(0,-1)]
            else:
                self.move = [(0,1)]
            self.slow = True
            self.first_move = True
        elif kind == "Knight":
            self.move = knight_move
            self.slow = True

def create_pieces():
    global alive_pieces
    for color in colors:
        for pawn_num in range(pawns):
            img_name = f"{color.lower()}_pawn_img"
            img_var = globals()[img_name]    
            alive_pieces.append(Piece(color,(pawn_num,pawn_row[color]),"pawn",img_var))
        for item_num in range(len(pieces_order)):
            img_name = f"{color.lower()}_{pieces_order[item_num].lower()}_img"
            img_var = globals()[img_name]
            alive_pieces.append(Piece(color,(item_num,other_row[color]),pieces_order[item_num],img_var))

def captures(capturing_piece,captured_piece):
    global alive_pieces
    capturing_piece.loc = captured_piece.loc
    alive_pieces.remove(captured_piece)

def do_grid():
    grid = [[0 for i in range(board_len)]for j in range(board_len)]
    for i in range(board_len):
        for j in range(board_len):
            if (i+j) %2 == 0:
                grid[i][j] = "."
            else:
                grid[i][j] = "#"
    for item in alive_pieces:
        x,y = item.loc
        grid[y][x] = item

    return grid

def move_pieces(current_piece,loc):
    global alive_pieces
    x,y = loc
    current_piece.loc = (x,y)
    if current_piece.kind == "pawn":
        current_piece.first_move = False

def next_turn():
    global turn_count
    turn_count += 1

def whose_turn():
    return(colors[turn_count%2])

def display_pieces():
    for item in alive_pieces:
        x,y = item.loc
        window.blit(item.image,(x*70,y*70))
    
def show_movement(piece):
    global selected_piece
    ava_sqr = []
    selected_piece = piece
    
    if piece.slow:
        x, y = piece.loc
        for dx, dy in piece.move:
            target_x = x + dx
            target_y = y + dy
            
            # Check bounds
            if 0 <= target_x < 8 and 0 <= target_y < 8:
                target_square = grid[target_y][target_x]
                
                if target_square in space:
                    pygame.draw.circle(window, circle_green, 
                                     (target_x * tile_size + tile_size/2, 
                                      target_y * tile_size + tile_size/2), 
                                     circle_radius)
                    ava_sqr.append((target_x,target_y))
                    
                    # Pawn double move on first move
                    if piece.kind == "pawn" and piece.first_move:
                        double_target_x = x + (dx * 2)
                        double_target_y = y + (dy * 2)
                        if 0 <= double_target_y < 8 and grid[double_target_y][double_target_x] in space:
                            pygame.draw.circle(window, circle_green,
                                             (double_target_x * tile_size + tile_size/2,
                                              double_target_y * tile_size + tile_size/2),
                                             circle_radius)
                            ava_sqr.append((target_x,target_y))
                            ava_sqr.append((double_target_x,double_target_y))
                
                elif target_square.color != piece.color:
                    pygame.draw.circle(window, circle_green,
                                     (target_x * tile_size + tile_size/2,
                                      target_y * tile_size + tile_size/2),
                                     circle_radius * 2, width=5)
                    ava_sqr.append((target_x,target_y))
    
    else:  # Sliding pieces
        x, y = piece.loc
        for dx, dy in piece.move:            
            for i in range(1, 8): 
                target_x = x + (dx * i)
                target_y = y + (dy * i)
                                
                if 0 <= target_x < 8 and 0 <= target_y < 8:
                    target_square = grid[target_y][target_x]
                    
                    if target_square in space:                        
                        pygame.draw.circle(window, circle_green,
                                         (target_x * tile_size + tile_size/2,
                                          target_y * tile_size + tile_size/2),
                                         circle_radius)
                        ava_sqr.append((target_x,target_y))
                    
                    elif target_square.color != piece.color:                        
                        pygame.draw.circle(window, circle_green,
                                         (target_x * tile_size + tile_size/2,
                                          target_y * tile_size + tile_size/2),
                                         circle_radius * 2, width=5)
                        ava_sqr.append((target_x,target_y))
                        break 
                    else:                        
                        break
                else:                    
                    break
    
    return ava_sqr
def display_board():
    for i in range(board_len):
        for j in range(board_len):
            
            if (i+j) %2 == 0:
                color = white
            else:
                color = black 
            
            pygame.draw.rect(window, color, (j*tile_size,i*tile_size,tile_size,tile_size))


running = True
create_pieces()
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONUP:
            loc = pygame.mouse.get_pos()
            x,y = loc
            loc_coord = ((x//tile_size),(y//tile_size))
            i,j = loc_coord
            selected_tile = grid[j][i]
            if selected_piece:
                if (i,j) in ava_sqr:
                    if type(selected_tile) == Piece and selected_tile.color != whose_turn():
                        captures(selected_piece,selected_tile)
                        next_turn()
                        selected_piece = None
                    else:
                        move_pieces(selected_piece,(i,j))
                        next_turn()
                        selected_piece = None
            elif selected_tile in space:
                pass
            elif selected_tile.color == whose_turn():
                selected_piece = selected_tile
                ava_sqr = show_movement(selected_piece)



            
    grid = do_grid()

    window.fill((0, 0, 0))
    display_board()
    display_pieces()
    if selected_piece:
        show_movement(selected_piece)    




    pygame.display.update()
pygame.quit()



# check
# capturing
# pawn shit
