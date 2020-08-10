from tkinter import *
from PIL import ImageTk, Image
import time

def f(r, c):
    return r*8+c

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
        self.colorSave=BG
        self.r=coord[0]
        self.c=coord[1]
        self.f=[self.r,self.c]
        self.cellNum = f(self.r, self.c)
        
        self.slength=50
        Canvas.__init__(self,master,width=self.slength,height=self.slength,bg=self.bgColor,highlightthickness=0,relief=RAISED)

        self.piece='none'
        # self.text = self.create_text(50/2,50/2,anchor = "center", text="", fill='black', font = ("Arial", 24))

        self.bind("<Button-1>",self.move)

        self.hasMoved = False

    def __str__(self):
        return self.piece

    def createPiece(self,pieceName, hasMoved=False, size=(50,50)):
        if pieceName=="none":
            return 0
        self.createImage(pieceName,size)
        self.piece = pieceName
        self.hasMoved = hasMoved
            
    def removePiece(self):
        self.piece = 'none'
        self.hasMoved = False
        self.delete(self.pic)
        # self.itemconfig(self.text,text="")

    def createImage(self,pieceName,size):
        filename = self.pics[pieceName]
        self.im = Image.open(filename)
        self.resizePic(size)
        self.img=ImageTk.PhotoImage(self.im)
        self.pic = self.create_image(self.slength/2,self.slength/2,anchor=CENTER,\
                                     image=self.img)

    def resizePic(self,size):
        self.im = self.im.resize(size,Image.ANTIALIAS)

    def highlight(self):
        self['bg']='darkolivegreen2'

    def unhighlight(self):
        self['bg']=self.colorSave

    def isHighlighted(self, Type):
        if Type == 'move':
            return self['bg']=='chartreuse2'
        elif Type == 'check':
            return self['bg']=='tomato2'

    def promote(self):
        self.master.unBindAll()
        self.master.qButton = Button(self.master, text='Queen',command=self.createQueen)
        self.master.rButton = Button(self.master, text='Rook',command=self.createRook)
        self.master.bButton = Button(self.master, text='Bishop',command=self.createBishop)
        self.master.kButton = Button(self.master, text='Knight',command=self.createKnight)
        self.master.conButton = Button(self.master, text='CONFIRM PIECE',command=self.confirmPiece)
        self.master.qButton.grid(row=8,column=0,columnspan=2)
        self.master.rButton.grid(row=8,column=2,columnspan=2)
        self.master.bButton.grid(row=8,column=4,columnspan=2)
        self.master.kButton.grid(row=8,column=6,columnspan=2)
        self.master.conButton.grid(row=9,column=2,columnspan=4)

    def createQueen(self):
        color = self.piece[0]
        self.removePiece()
        self.createPiece(color+'quen', True)

    def createRook(self):
        color = self.piece[0]
        self.removePiece()
        self.createPiece(color+'rook', True)

    def createBishop(self):
        color = self.piece[0]
        self.removePiece()
        self.createPiece(color+'bish', True)

    def createKnight(self):
        color = self.piece[0]
        self.removePiece()
        self.createPiece(color+'nite', True)

    def confirmPiece(self):
        if self.piece[1:] == 'pawn':
            return 0
        self.master.qButton.grid_remove()
        self.master.rButton.grid_remove()
        self.master.bButton.grid_remove()
        self.master.kButton.grid_remove()
        self.master.conButton.grid_remove()
        self.master.bindAll()
        self.master.toggleTurn()

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
                    # self.master.copyBoard = self.master.cells[:]
                    self.master.copyBoard = self.master.copyCells()
                    if (pieceClicked[1].piece[1:]=='pawn' and self.piece=='none' and pieceClicked[1].r-self.r==1 and abs(pieceClicked[1].c-self.c)==1):
                        self.master.cells[f(pieceClicked[1].r, self.c)].removePiece()  # en passant check
                        
                    if pieceClicked[1].piece[1:] == 'king':   # castle rook move
                        if self.cellNum - pieceClicked[1].cellNum == 2:
                            self.master.cells[self.cellNum-1].createPiece(color + 'rook', True)
                            self.master.cells[63].removePiece()
                        elif self.cellNum - pieceClicked[1].cellNum == -2:
                            self.master.cells[self.cellNum+1].createPiece(color + 'rook', True)
                            self.master.cells[56].removePiece()
                    if self.piece != 'none':  # in case of captures
                        self.removePiece()
                    self.createPiece(pieceClicked[1].piece, True)   # normal moving
                    pieceClicked[1].removePiece()
                    temp = self.master.gameMoves[:]
                    self.master.gameMoves=[self.piece, pieceClicked[1], self]
                    if self.master.inCheck(['w','b'][self.master.turn]):
                        self.master.revertMove()
                        pieceClicked[1].unhighlight()
                        self.master.gameMoves=temp[:]
                    else:

                        if self.r==0 and self.piece[1:]=='pawn':  # promotion
                            self.promote()
                        else:
                            self.master.toggleTurn()

                        self.master.unhighlightKeySquares()
                        self.master.highlightKeySquares(pieceClicked[1], self, 'move')
                else:
                    pieceClicked[1].unhighlight()
            else:                
                pieceClicked[1].unhighlight()
                if self == pieceClicked[1]:  # if same piece
                    pieceClicked = (False, None)
                    return
                self.highlight()
                pieceClicked = (True, self) 
                return 

            pieceClicked = (False, None)
            
        return

class chessBoard(Frame):
    def __init__(self,master):
        self.letters = ['w','b']
        Frame.__init__(self,master)
        self.grid()
        self.cells=[]
        
        self.gameMoves = []
        
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
        self.unBindAll()
        self.after(1000, self.flipBoard)
        # self.flipBoard()
        self.bindAll()
        self.turn = (self.turn+1)%2

    def highlightKeySquares(self, srcSquare, dstSquare, Type):
        if Type == 'move':
            color = ['chartreuse2', 'chartreuse3']
        if Type == 'check':
            color = ['chartreuse3', 'tomato2']

        srcSquare['bg'] = color[0]
        dstSquare['bg'] = color[1]
        srcSquare.colorSave = srcSquare['bg']
        dstSquare.colorSave = dstSquare['bg']
        
    def unhighlightKeySquares(self):
        if len(self.gameMoves) > 0:
            srcSquare = self.gameMoves[1]
            dstSquare = self.gameMoves[2]
            srcSquare.colorSave = srcSquare.bgColor
            dstSquare.colorSave = dstSquare.bgColor
            srcSquare.unhighlight()
            dstSquare.unhighlight()

    def flipBoard(self, changeGrid=True):
        if changeGrid:
            for i in range(8):
                for j in range(8):
                    self.cells[f(i,j)].grid_remove()
        self.cells=self.rotateMat()
        if changeGrid:
            for i in range(8):
                for j in range(8):
                    newCell = self.cells[f(i,j)]
                    newCell.grid(row=i,column=j)
                    newCell.createPiece(newCell.piece, newCell.hasMoved)

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
                temp[d[i]][d[j]].r = d[i]
                temp[d[i]][d[j]].c = d[j]
                temp[d[i]][d[j]].f = [d[i],d[j]]
                temp[d[i]][d[j]].cellNum = f(d[i],d[j])
        l=[]
        for i in range(8):
            for j in range(8):
                l.append(temp[i][j])
        return l
    
    def genPawnMoves(self, color, srcRow, srcCol):
        pawnMoves = []

        if self.cells[f(srcRow-1,srcCol)].piece == 'none':
            if srcRow+1 == 7 and self.cells[f(srcRow-2,srcCol)].piece == 'none':
                pawnMoves.append([srcRow-2, srcCol])
            pawnMoves.append([srcRow-1, srcCol])
        if srcCol-1 > -1:
            capturePiece = self.cells[f(srcRow-1,srcCol-1)].piece 
            if capturePiece[0] != color and capturePiece != 'none':
                pawnMoves.append([srcRow-1, srcCol-1])
        if srcCol+1 < 8:
            capturePiece = self.cells[f(srcRow-1,srcCol+1)].piece
            if capturePiece[0] != color and capturePiece != 'none':
                pawnMoves.append([srcRow-1, srcCol+1])
        if srcCol+1 < 8:
            if srcRow==3:
                if self.cells[f(srcRow-1,srcCol+1)].piece[0] != color:
                    if self.gameMoves[0]==['b','w'][self.turn] + 'pawn':
                        if self.gameMoves[1].f==[1,srcCol+1] and self.gameMoves[2].f==[3,srcCol+1]:
                            pawnMoves.append([srcRow-1, srcCol+1])
        if srcCol-1 > -1:
            if srcRow==3:
                if self.cells[f(srcRow-1,srcCol-1)].piece[0] != color:
                    if self.gameMoves[0]==['b','w'][self.turn] + 'pawn':
                        if self.gameMoves[1].f==[1,srcCol-1] and self.gameMoves[2].f==[3,srcCol-1]:
                            pawnMoves.append([srcRow-1, srcCol-1])
                
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
                    c += dc[i]
                    continue
                else:
                    if (self.cells[f(r,c)].piece[0]==color):
                        break
                    else:
                        bishMoves.append([r,c])
                        break
        return bishMoves

    def genRookMoves(self, color, srcRow, srcCol):
        rookMoves = []
        dr = [1, -1, 0, 0]
        dc = [0, 0, 1, -1]
        for i in range(4):
            r = srcRow+dr[i]
            c = srcCol+dc[i]
            while (True):
                if (r > 7 or r < 0 or c > 7 or c < 0):
                    break
                if self.cells[f(r,c)].piece == 'none':
                    rookMoves.append([r, c])
                    r += dr[i]
                    c += dc[i]
                    continue
                else:
                    if (self.cells[f(r,c)].piece[0]==color):
                        break
                    else:
                        rookMoves.append([r,c])
                        break
        return rookMoves

    def genQuenMoves(self, color, srcRow, srcCol):
        return self.genRookMoves(color, srcRow, srcCol) + self.genBishMoves(color, srcRow, srcCol)

    def genNiteMoves(self, color, srcRow, srcCol):
        niteMoves = []
        dr = [2, 2, 1, 1, -2, -2, -1, -1]
        dc = [1, -1, 2, -2, 1, -1, 2, -2]
        for i in range(8):
            r = srcRow + dr[i]
            c = srcCol + dc[i]
            if (r > 7 or r < 0 or c > 7 or c < 0):
                continue
            if (self.cells[f(r,c)].piece[0]==color):
                continue
            niteMoves.append([r,c])
        return niteMoves

    def genKingMoves(self, color, srcRow, srcCol):
        kingMoves = []
        dr = [1, 1, 1, 0, -1, -1, -1, 0]
        dc = [1, -1, 0, 1, 1, -1, 0, -1]
        for i in range(8):
            r = srcRow + dr[i]
            c = srcCol + dc[i]
            if (r > 7 or r < 0 or c > 7 or c < 0):
                continue
            if (self.cells[f(r,c)].piece[0]==color):
                continue
            kingMoves.append([r,c])
        
        if self.cells[f(srcRow,srcCol)].hasMoved == False:
            if color == "w":
                if (f(srcRow, srcCol) == 60 and self.cells[63].piece == color+'rook' and self.cells[63].hasMoved == False and
                self.cells[61].piece == 'none' and self.cells[62].piece == 'none'):
                    kingMoves.append([srcRow,srcCol+2])
                if (f(srcRow, srcCol) == 60 and self.cells[56].piece == color+'rook' and self.cells[56].hasMoved == False and
                self.cells[59].piece == 'none' and self.cells[58].piece == 'none' and self.cells[57].piece == 'none'):
                    kingMoves.append([srcRow,srcCol-2])
            else:
                if (f(srcRow, srcCol) == 59 and self.cells[56].piece == color+'rook' and self.cells[56].hasMoved == False and
                self.cells[58].piece == 'none' and self.cells[57].piece == 'none'):
                    kingMoves.append([srcRow,srcCol-2])
                if (f(srcRow, srcCol) == 59 and self.cells[63].piece == color+'rook' and self.cells[63].hasMoved == False and
                self.cells[60].piece == 'none' and self.cells[61].piece == 'none' and self.cells[62].piece == 'none'):
                    kingMoves.append([srcRow,srcCol+2])
        
        return kingMoves
        
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
        if piece[1:] == 'rook':
            rookMoves = self.genRookMoves(color, r1, c1)
            if move in rookMoves:
                legal = True
        if piece[1:] == 'nite':
            knightMoves = self.genNiteMoves(color, r1, c1)
            if move in knightMoves:
                legal = True
        if piece[1:] == 'quen':
            queenMoves = self.genQuenMoves(color, r1, c1)
            if move in queenMoves:
                legal = True
        if piece[1:] == 'king':
            kingMoves = self.genKingMoves(color, r1, c1)
            if move in kingMoves:
                legal = True

        # check for check ;)

        return legal

    def unBindAll(self):
        for i in range(8):
            for j in range(8):
                self.cells[f(i,j)].unbind("<Button-1>")

    def bindAll(self):
        for i in range(8):
            for j in range(8):
                self.cells[f(i,j)].bind("<Button-1>", self.cells[f(i,j)].move)

    def revertMove(self):
        for i in self.cells:
            if i.piece != 'none':
                i.removePiece()
        for i in range(8):
            for j in range(8):
                self.cells[f(i,j)].createPiece(self.copyBoard[f(i,j)][0], self.copyBoard[f(i,j)][1])

    def inCheck(self, colorToCheck):
        self.toggleTurn()
        kingLoc = 0
        oColor = 'x'
        if (colorToCheck=='w'):
            oColor='b'
        else:
            oColor='w'
        for i in self.cells:
            if i.piece==colorToCheck+'king':
                kingLoc=i.f
        allMoves = []
        for i in self.cells:
            if i.piece[0]!=colorToCheck and i.piece != 'none':
                if i.piece[1:]=='pawn':
                    allMoves += self.genPawnMoves(oColor, i.r, i.c)
            if i.piece[0]!=colorToCheck and i.piece != 'none':
                if i.piece[1:]=='bish':
                    allMoves += self.genBishMoves(oColor, i.r, i.c)
            if i.piece[0]!=colorToCheck and i.piece != 'none':
                if i.piece[1:]=='king':
                    allMoves += self.genKingMoves(oColor, i.r, i.c)
            if i.piece[0]!=colorToCheck and i.piece != 'none':
                if i.piece[1:]=='nite':
                    allMoves += self.genNiteMoves(oColor, i.r, i.c)
            if i.piece[0]!=colorToCheck and i.piece != 'none':
                if i.piece[1:]=='rook':
                    allMoves += self.genRookMoves(oColor, i.r, i.c)
            if i.piece[0]!=colorToCheck and i.piece != 'none':
                if i.piece[1:]=='quen':
                    allMoves += self.genQuenMoves(oColor, i.r, i.c)
            

        self.toggleTurn()
        if kingLoc in allMoves:
            return True
        else:
            return False

    def copyCells(self):
        a = []
        for i in self.cells:
            a.append([i.piece, i.hasMoved])
        return a

def play_chess():
    root = Tk()
    root.title('Chess')
    game = chessBoard(root)
    root.mainloop()

play_chess()