def show_movevment(piece):
    pass

dia_move = [(1,1),(-1,-1),(1,-1),(-1,1)]
str_move = [(1,0),(0,1),(-1,0),(0,-1)]

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
    
                if selected_piece:
                if "ava_sqr" in globals() and selected_tile in space:
                    if (i,j) in ava_sqr:
                        move_pieces(selected_piece,(i,j))
                        next_turn()
                    else:
                        selected_piece = None
                elif selected_tile.color != selected_piece.color:
                    captures(selected_piece,selected_tile)
                    next_turn()
                else:
                    current_piece = selected_tile
                    ava_sqr = show_movement(current_piece)
            elif selected_tile.color == whose_turn():
                selected_piece = selected_tile