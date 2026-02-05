import pygame
import pyautogui
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
        self.ava_sqr = []
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
        elif kind == "Knight":
            self.move = knight_move
            self.slow = True

class Pawn(Piece):
    def __init__(self, color, location, kind, image):
        super().__init__(color, location, kind, image)
        self.slow = True
        self.first_move = True
        if self.color == "Black":
            self.move = [(0,-1)]
        else:
            self.move = [(0,1)]

class KingEndanger(Exception):
    pass

class Checkmated (Exception):
    pass

def create_pieces():
    global alive_pieces
    for color in colors:
        for pawn_num in range(pawns):
            img_name = f"{color.lower()}_pawn_img"
            img_var = globals()[img_name]    
            alive_pieces.append(Pawn(color,(pawn_num,pawn_row[color]),"pawn",img_var))
        for item_num in range(len(pieces_order)):
            img_name = f"{color.lower()}_{pieces_order[item_num].lower()}_img"
            img_var = globals()[img_name]
            alive_pieces.append(Piece(color,(item_num,other_row[color]),pieces_order[item_num],img_var))

def captures(capturing_piece,captured_piece):
    global alive_pieces
    global running
    if captured_piece.kind != "King":
        capturing_piece.loc = captured_piece.loc
        alive_pieces.remove(captured_piece)
    else:
            running = False
            
def CheckMate():
    global running
    tiles = []
    for item in alive_pieces:
        if item.color == whose_turn():
            tiles += item.ava_sqr
    if len(tiles) == 0:
        running = False

def KingSafe(color_to_check):
    """Check if the given color's king is under attack by opponent pieces."""
    # Find the king of the color being checked
    king = None
    for piece in alive_pieces:
        if piece.color == color_to_check and piece.kind == "King":
            king = piece
            break
    
    if not king:
        return  # King not found (shouldn't happen)
    
    king_x, king_y = king.loc
    
    # Check all opponent pieces to see if they can attack the king
    for attacker in alive_pieces:
        if attacker.color == color_to_check:  # Skip own color
            continue
        
        # Check if this opponent piece threatens the king
        if attacker.slow:  # Knight, King, Pawn
            ax, ay = attacker.loc
            for dx, dy in attacker.move:
                if attacker.kind == "pawn":
                    # Pawns attack diagonally, and direction depends on color
                    if attacker.color == "White":
                        check_dirs = [(-1, -1), (1, -1)]  # White pawns attack upward-diagonally
                    else:
                        check_dirs = [(-1, 1), (1, 1)]  # Black pawns attack downward-diagonally
                    for pdx, pdy in check_dirs:
                        if ax + pdx == king_x and ay + pdy == king_y:
                            raise KingEndanger
                else:
                    if ax + dx == king_x and ay + dy == king_y:
                        raise KingEndanger
        else:  # Sliding pieces (Rook, Bishop, Queen)
            ax, ay = attacker.loc
            for dx, dy in attacker.move:
                for i in range(1, 8):
                    tx = ax + (dx * i)
                    ty = ay + (dy * i)
                    
                    if not (0 <= tx < 8 and 0 <= ty < 8):
                        break
                    
                    if tx == king_x and ty == king_y:
                        raise KingEndanger
                    
                    # Check if path is blocked
                    target = grid[ty][tx]
                    if target not in space:  # Hit another piece
                        break
            
def UpdateLoc(piece):
    for col in range(len(grid)):
        if piece in grid[col]:
            piece.loc = grid[col][grid[col].index(piece)].loc

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
    if current_piece.kind == "pawn" and current_piece.first_move:
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
        piece.ava_sqr = []
        piece.ava_sqr += ava_sqr
    return ava_sqr
def display_board():
    for i in range(board_len):
        for j in range(board_len):
            
            if (i+j) %2 == 0:
                color = white
            else:
                color = black 
            
            pygame.draw.rect(window, color, (j*tile_size,i*tile_size,tile_size,tile_size))

fps_count = pygame.time.Clock()
running = True
create_pieces()

while running:
    fps_count.tick(30)

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
                    # Save original state before attempting move
                    original_loc = selected_piece.loc
                    original_captured = None
                    
                    if type(selected_tile) in [Piece,Pawn] and selected_tile.color != whose_turn():
                        # Capture attempt
                        original_captured = selected_tile
                        try:
                            captures(selected_piece, selected_tile)
                            grid = do_grid()  # Update grid after capture
                            KingSafe(whose_turn())  # Check if our king is safe
                        except KingEndanger:
                            # Revert capture
                            selected_piece.loc = original_loc
                            alive_pieces.append(original_captured)
                            selected_piece = None
                        else:    
                            next_turn()
                            selected_piece = None
                    else:
                        # Normal move attempt
                        try:
                            move_pieces(selected_piece, (i, j))
                            grid = do_grid()  # Update grid after move
                            KingSafe(whose_turn())  # Check if our king is safe
                        except KingEndanger:
                            # Revert move
                            selected_piece.loc = original_loc
                            selected_piece = None
                        else:
                            next_turn()
                            selected_piece = None
                elif selected_tile in space or (type(selected_tile) in [Piece,Pawn] and selected_tile.color != whose_turn()):
                    selected_piece = None
                else:
                    selected_piece = selected_tile
            elif selected_tile in space:
                pass
            elif type(selected_tile) in [Piece,Pawn] and selected_tile.color == whose_turn():
                selected_piece = selected_tile
                ava_sqr = show_movement(selected_piece)

            
    grid = do_grid()

    window.fill((0, 0, 0))
    display_board()
    display_pieces()
    if selected_piece:
        show_movement(selected_piece)    




    pygame.display.update()
else:
    next_turn()
    pyautogui.alert(f"{whose_turn()} won the game")
pygame.quit()


# check
# pawn shit
