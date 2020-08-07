from tkinter import *
from PIL import ImageTk, Image

def f(x, y):
    return x*8+y

pieceClicked = (False, None)

class Piece(Canvas):

    pics = {\
            'bpawn':'pieces/bPawn.png',\
            'bbish':'pieces/bBishop.png',\
            'bking':'pieces/bKing.png',\
            'brook':'pieces/bRook.png',\
            'bnite':'pieces/bKnight.png',\
            'bquen':'pieces/bQueen.png',\
            'wpawn':'pieces/wPawn.png',\
            'wbish':'pieces/wBishop.png',\
            'wking':'pieces/wKing.png',\
            'wrook':'pieces/wRook.png',\
            'wnite':'pieces/wKnight.png',\
            'wquen':'pieces/wQueen.png',\
            }
    
    def __init__(self,master,BG,coord):
        self.bgColor=BG
        self.r=coord[0]
        self.c=coord[1]
        self.f=f(self.r,self.c)
        self.slength=50
        Canvas.__init__(self,master,width=self.slength,height=self.slength,bg=self.bgColor,highlightthickness=0,relief=RAISED)

        self.piece='none'
        # self.text = self.create_text(50/2,50/2,anchor = "center", text="", fill='black', font = ("Arial", 24))

        self.bind("<Button-1>",self.move)

    def __str__(self):
        return self.piece

    def createPiece(self,pieceName, size=(50,50)):
        if pieceName=="none":
            return 0
        self.createImage(pieceName,size)
        self.piece = pieceName

    def createImage(self,pieceName,size):
        filename = self.pics[pieceName]
        self.im = Image.open(filename)
        self.resizePic(size)
        self.img=ImageTk.PhotoImage(self.im)
        self.pic = self.create_image(self.slength/2,self.slength/2,anchor=CENTER,\
                                     image=self.img)

    def resizePic(self,size):
        self.im = self.im.resize(size,Image.ANTIALIAS)

    def removePiece(self):
        self.piece = 'none'
        self.delete(self.pic)
        # self.itemconfig(self.text,text="")

    def highlight(self):
        self['bg']='lightgreen'

    def unhighlight(self):
        self['bg']=self.bgColor

    def isHighlighted(self):
        return self['bg']=='lightgreen'

    def move(self, misc=''):
        global pieceClicked

        colors = ['w','b']
        color = colors[self.master.turn]
        
        matchingColors = self.piece[0] == color
        
        if pieceClicked[0] == False:   # if first click
            if self.piece != "none":
                if matchingColors:  # if clicking own piece
                    self.highlight()
                    pieceClicked = (True,self)
        else:   # if second click            
            if matchingColors == False:
                if (self.master.validMove(  pieceClicked[1].r,pieceClicked[1].c, \
                                            self.r           ,self.c            )):
                    self.createPiece(pieceClicked[1].piece)
                    pieceClicked[1].removePiece()
                    self.master.toggleTurn()
            else:
                pieceClicked[1].unhighlight()
                if self == pieceClicked[1]:  # if same piece
                    pieceClicked = (False, None)
                    return
                self.highlight()
                pieceClicked = (True, self) 
                return 

            pieceClicked[1].unhighlight()
            pieceClicked = (False, None)
            
        return

class chessBoard(Frame):
    def __init__(self,master):
        self.letters = ['w','b']
        Frame.__init__(self,master)
        self.grid()
        self.cells=[]
        for i in range(8):
            for j in range(8):
                if (i%2==0 and j%2==0) or (i%2==1 and j%2==1):
                    color='blanched almond'
                else:
                    color='olive drab'
                self.cells.append(Piece(self,color,(i,j)))
                self.cells[i*8+j].grid(row=i,column=j)
        self.cells[0].createPiece('brook')
        self.cells[1].createPiece('bnite')
        self.cells[2].createPiece('bbish')
        self.cells[3].createPiece('bquen')
        self.cells[4].createPiece('bking')
        self.cells[5].createPiece('bbish')
        self.cells[6].createPiece('bnite')
        self.cells[7].createPiece('brook')
        for i in range(8):
            self.cells[f(1,i)].createPiece('bpawn')
            self.cells[f(6,i)].createPiece('wpawn')
        self.cells[f(7,0)].createPiece('wrook')
        self.cells[f(7,1)].createPiece('wnite')
        self.cells[f(7,2)].createPiece('wbish')
        self.cells[f(7,3)].createPiece('wquen')
        self.cells[f(7,4)].createPiece('wking')
        self.cells[f(7,5)].createPiece('wbish')
        self.cells[f(7,6)].createPiece('wnite')
        self.cells[f(7,7)].createPiece('wrook')
        self.turn = 0

    def toggleTurn(self):
        self.turn = (self.turn+1)%2
        self.flipBoard()

    def unhighlight(self):
        for i in self.cells:
            i.unhighlight()

    def flipBoard(self):
        for i in range(8):
            for j in range(8):
                self.cells[f(i,j)].grid_remove()
        self.cells=self.rotateMat()
        for i in range(8):
            for j in range(8):
                self.cells[f(i,j)].grid(row=i,column=j)
                self.cells[f(i,j)].createPiece(self.cells[f(i,j)].piece)

    def rotateMat(self):
        d = {0:7,1:6,2:5,3:4,4:3,5:2,6:1,7:0}
        l = []
        for i in range(8):
            l.append([])
            for j in range(8):
                l[i].append(self.cells[f(i,j)])
        temp=[]
        for i in range(8):
            temp.append([])
            for j in range(8):
                temp[i].append(0)
        for i in range(8):
            for j in range(8):
                temp[d[i]][d[j]]=l[i][j]
        l=[]
        for i in range(8):
            for j in range(8):
                l.append(temp[i][j])
        return l
    
    def genPawnMoves(self, color, srcRow, srcCol):
        pawnMoves = []
        
        if color == "w":
            if self.cells[f(srcRow-1,srcCol)].piece == 'none':
                if srcRow+1 == 7 and self.cells[f(srcRow-2,srcCol)].piece == 'none':
                    pawnMoves.append([srcRow-2, srcCol])
                pawnMoves.append([srcRow-1, srcCol])
            if srcCol+1 > 1 and self.cells[f(srcRow-1,srcCol-1)].piece != 'none':
                pawnMoves.append([ srcRow-1, srcCol-1])
            if srcCol+1 < 8 and self.cells[f(srcRow-1,srcCol+1)].piece != 'none':
                pawnMoves.append([srcRow-1, srcCol+1])
        else:
            if self.cells[f(srcRow+1,srcCol)].piece == 'none':
                if srcRow+1 == 2 and self.cells[f(srcRow+2,srcCol)].piece == 'none':
                    pawnMoves.append([srcRow+2, srcCol])
                pawnMoves.append([srcRow+1, srcCol])
            if srcCol+1 > 1 and self.cells[f(srcRow+1,srcCol-1)].piece != 'none':
                pawnMoves.append([srcRow+1, srcCol-1])
            if srcCol+1 < 8 and self.cells[f(srcRow+1,srcCol+1)].piece != 'none':
                pawnMoves.append([srcRow+1, srcCol+1])
                
        return pawnMoves

    def genBishMoves(self, color, srcRow, srcCol):
        bishMoves = []
        dr = [1, 1, -1, -1]
        dc = [1, -1, 1, -1]
        for i in range(4):
            r = srcRow+dr[i]
            c = srcCol+dc[i]
            while (True):
                if (r > 7 or r < 0 or c > 7 or c < 0):
                    break
                if self.cells[f(r,c)].piece == 'none':
                    bishMoves.append([r, c])
                    r += dr[i]
                    c += dr[i]
                    continue
                else:
                    if (self.cells[f(r,c)].piece[0]==color):
                        break
                    else:
                        bishMoves.append([r,c])
                        break
        return bishMoves

        
    def searchForPieces(self, color):
        pawns = [], bishops = [], knights = [], rooks = [], queens = [], king = []

        for i in range(8):
            for j in range(8):
                temp = self.cells[f(i,j)].piece
                if temp == color + 'pawn':
                    pawns.append([i,j])
                elif temp == color + 'bish':
                    bishops.append([i,j])
                elif temp == color + 'nite':
                    knights.append([i,j])
                elif temp == color + 'rook':
                    rooks.append([i,j])
                elif temp == color + 'quen':
                    queens.append([i,j])
                elif temp == color + 'king':
                    king.append([i,j])
                    
        return [pawns, bishops, knights, rooks, queens, king]
        
    def validMove(self, r1, c1, r2, c2):
        ''' Given a move, it returns whether the move is valid
        by generating all possible moves and checking if the 
        given one is one of them.'''

        # Generating all possible moves

        color = ['w','b'][self.turn]
        piece = self.cells[f(r1,c1)].piece
        move = [r2, c2]
        legal = False  # only based on movement for now
        
        if piece[1:] == 'pawn':
            pawnMoves = self.genPawnMoves(color, r1, c1)
            if move in pawnMoves:
                legal = True
        if piece[1:] == 'bish':
            bishopMoves = self.genBishMoves(color, r1, c1)
            if move in bishopMoves:
                legal = True
        if piece[1:] == 'nite':
            knightMoves = self.genKnightMoves(color, r1, c1)
            if move in knightMoves:
                legal = True
        if piece[1:] == 'quen':
            queenMoves = self.genQueenMoves(color, r1, c1)
            if move in queenMoves:
                legal = True
        if piece[1:] == 'king':
            kingMoves = self.genKingMoves(color, r1, c1)
            if move in kingMoves:
                legal = True


        # check for check ;)

        return legal



def play_chess():
    root = Tk()
    root.title('Chess')
    game = chessBoard(root)
    root.mainloop()


play_chess()