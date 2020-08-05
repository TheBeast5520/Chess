from tkinter import *
from PIL import ImageTk, Image

def cL(coord):
    return coord[0]*8+coord[1]

class chessPiece(Canvas):
    pics = {\
            'bpawn':'pieces/bPawn.png',\
            'bbish':'pieces/bBishop.png',\
            'bking':'pieces/bKing.png',\
            'brook':'pieces/bRook.png',\
            'bknit':'pieces/bKnight.png',\
            'bquen':'pieces/bQueen.png',\
            'wpawn':'pieces/wPawn.png',\
            'wbish':'pieces/wBishop.png',\
            'wking':'pieces/wKing.png',\
            'wrook':'pieces/wRook.png',\
            'wknit':'pieces/wKnight.png',\
            'wquen':'pieces/wQueen.png',\
            }
    def __init__(self,master,BG,coord):
        self.bgColor = BG
        self.coord=coord
        self.cLoc=coord[0]*8+coord[1]
        self.width=50
        self.height=50
        Canvas.__init__(self,master,width=self.width,height=self.height,bg=BG,\
                        highlightthickness=0,relief=RAISED)
        self.piece = 'none'
        self.bind("<Button-1>",self.move)
        self.firstMoveOver='NA'
        self.hasMoved = False

    def createPiece(self,pieceName, size=(50,50)):
        self.createImage(pieceName,size)
        self.piece = pieceName

    def createImage(self,pieceName,size):
        filename = self.pics[pieceName]
        self.im = Image.open(filename)
        self.resizePic(size)
        self.img=ImageTk.PhotoImage(self.im)
        self.pic = self.create_image(self.width/2,self.height/2,anchor=CENTER,\
                                     image=self.img)

    def resizePic(self,size):
        self.im = self.im.resize(size,Image.ANTIALIAS)

    def removePiece(self):
        self.piece = 'none'
        self.delete(self.pic)

    def move(self, misc = ''):
        if self['bg']=='lightgreen':
            self.unhighlight()
            self.master.lastCell=-1
            return 0
        if not self.master.hasHighlighted:
            self.master.cells[self.master.lastCell].unhighlight()
            self.highlight()
            self.master.lastCell=self.cLoc
        else:
            if self.master.lastCell==-1:
                return 0
            if self.master.validMove(self.master.cells[self.master.lastCell], self):
                self.master.cells[self.master.lastCell].unhighlight()
                self.highlight()
                self.createPiece(self.master.cells[self.master.lastCell].piece)
                self.master.cells[self.master.lastCell].removePiece()
                self.firstMoveOver, self.master.cells[self.master.lastCell].firstMoveOver=\
                                    self.master.cells[self.master.lastCell].firstMoveOver, self.firstMoveOver
                if (self.piece=='bpawn' and self.coord[0]==7) or (self.piece=='wpawn' and self.coord[0]==0):
                    self.promote()
                self.master.lastCell=self.cLoc
                self.master.toggleTurn()
##            else:
##                self.master.cells[self.master.lastCell].unhighlight()
##                self.master.lastCell=self.cLoc
##                self.highlight()
            

    def highlight(self):
        self['bg']='lightgreen'
        self.master.hasHighlighted = True

    def unhighlight(self):
        self['bg']=self.bgColor
        self.master.hasHighlighted = False

    def promote(self):
        self.master.qButton = Button(self.master, text='Queen',command=self.createQueen)
        self.master.rButton = Button(self.master, text='Rook',command=self.createRook)
        self.master.bButton = Button(self.master, text='Bishop',command=self.createBishop)
        self.master.kButton = Button(self.master, text='Knight',command=self.createKnight)
        self.master.conButton = Button(self.master, text='CONFIRM PIECE',command=self.conPiece)
        self.master.qButton.grid(row=8,column=0,columnspan=2)
        self.master.rButton.grid(row=8,column=2,columnspan=2)
        self.master.bButton.grid(row=8,column=4,columnspan=2)
        self.master.kButton.grid(row=8,column=6,columnspan=2)
        self.master.conButton.grid(row=9,column=2,columnspan=4)

    def createQueen(self):
        if self.piece[0]=='w':
            self.createPiece('wquen')
        else:
            self.createPiece('bquen')

    def createRook(self):
        if self.piece[0]=='w':
            self.createPiece('wrook')
        else:
            self.createPiece('brook')

    def createBishop(self):
        if self.piece[0]=='w':
            self.createPiece('wbish')
        else:
            self.createPiece('bbish')

    def createKnight(self):
        if self.piece[0]=='w':
            self.createPiece('wknit')
        else:
            self.createPiece('bknit')

    def conPiece(self):
        if self.piece == 'bpawn' or self.piece=='wpawn':
            return 0
        self.master.qButton.grid_remove()
        self.master.rButton.grid_remove()
        self.master.bButton.grid_remove()
        self.master.kButton.grid_remove()
        self.master.conButton.grid_remove()

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
                self.cells.append(chessPiece(self,color,(i,j)))
                self.cells[i*8+j].grid(row=i,column=j)
        self.cells[0].createPiece('brook')
        self.cells[1].createPiece('bknit')
        self.cells[2].createPiece('bbish')
        self.cells[3].createPiece('bquen')
        self.cells[4].createPiece('bking')
        self.cells[5].createPiece('bbish')
        self.cells[6].createPiece('bknit')
        self.cells[7].createPiece('brook')
        for i in range(8):
            self.cells[cL((1,i))].createPiece('bpawn')
            self.cells[cL((6,i))].createPiece('wpawn')
        self.cells[cL((7,0))].createPiece('wrook')
        self.cells[cL((7,1))].createPiece('wknit')
        self.cells[cL((7,2))].createPiece('wbish')
        self.cells[cL((7,3))].createPiece('wquen')
        self.cells[cL((7,4))].createPiece('wking')
        self.cells[cL((7,5))].createPiece('wbish')
        self.cells[cL((7,6))].createPiece('wknit')
        self.cells[cL((7,7))].createPiece('wrook')
        self.lastCell = -1
        self.turn = 0
        self.hasHighlighted = False
        

    def toggleTurn(self):
        self.update_pState()
        self.turn = (self.turn+1)%2

    def validMove(self, oCell, nCell):
        if oCell.piece[0]!=self.letters[self.turn]:
            return False
        if self.letters[self.turn]==nCell.piece[0]:
            return False
        if oCell.piece=='wpawn':
            return self.validMoveWP(oCell, nCell)
        elif oCell.piece=='bpawn':
            return self.validMoveBP(oCell, nCell)
        elif oCell.piece=='wbish':
            return self.validMoveB(oCell, nCell)
        elif oCell.piece=='bbish':
            return self.validMoveB(oCell, nCell)
        elif oCell.piece=='wrook':
            return self.validMoveR(oCell, nCell)
        elif oCell.piece=='brook':
            return self.validMoveR(oCell, nCell)
        elif oCell.piece=='wquen':
            return self.validMoveQ(oCell, nCell)
        elif oCell.piece=='bquen':
            return self.validMoveQ(oCell, nCell)
        else:
            return False

    def validMoveWP(self, oCell, nCell):
        # check for capture
        if abs(oCell.coord[1]-nCell.coord[1])==1 and \
             oCell.coord[0]-nCell.coord[0]==1 and \
             nCell.piece[0] == 'b':
            self.toFINISHED(oCell.coord)
            return True
        # check for normal move
        if oCell.coord[1]==nCell.coord[1]:
            if nCell.piece!='none':
                return False
            if oCell.coord[0]==6:
                if nCell.coord[0]-oCell.coord[0]==-2:
                    if self.cells[cL((5,oCell.coord[1]))].piece != 'none':
                        return False
                    self.toCURRENT(oCell.coord)
                    return True
                elif nCell.coord[0]-oCell.coord[0]==-1:
                    self.toFINISHED(oCell.coord)
                    return True
            elif nCell.coord[0]-oCell.coord[0]==-1:
                    self.toFINISHED(oCell.coord)
                    return True
        # check for amphasant
        if (oCell.coord[0]==3 and nCell.coord[0]==2) and \
           abs(oCell.coord[1]-nCell.coord[1])==1 and \
           self.cells[cL((oCell.coord[0],nCell.coord[1]))].piece == "bpawn" and \
           self.cells[cL((oCell.coord[0],nCell.coord[1]))].firstMoveOver=='current':
            self.toFINISHED(oCell.coord)
            self.cells[cL((oCell.coord[0],nCell.coord[1]))].removePiece()
            return True
        return False

    def validMoveBP(self, oCell, nCell):
        # check for capture
        if abs(oCell.coord[1]-nCell.coord[1])==1 and \
             oCell.coord[0]-nCell.coord[0]==-1 and \
             nCell.piece[0] == 'w':
            self.toFINISHED(oCell.coord)
            return True
        # check for normal move
        if oCell.coord[1]==nCell.coord[1]:
            if nCell.piece!='none':
                return False
            if oCell.coord[0]==1:
                if nCell.coord[0]-oCell.coord[0]==2:
                    if self.cells[cL((2,oCell.coord[1]))].piece != 'none':
                        return False
                    self.toCURRENT(oCell.coord)
                    return True
                elif nCell.coord[0]-oCell.coord[0]==1:
                    self.toFINISHED(oCell.coord)
                    return True

            elif nCell.coord[0]-oCell.coord[0]==1:
                    self.toFINISHED(oCell.coord)
                    return True
        # check for amphasant
        if (oCell.coord[0]==4 and nCell.coord[0]==5) and \
           abs(oCell.coord[1]-nCell.coord[1])==1 and \
           self.cells[cL((oCell.coord[0],nCell.coord[1]))].piece == 'wpawn' and \
           self.cells[cL((oCell.coord[0],nCell.coord[1]))].firstMoveOver=='current':
            self.toFINISHED(oCell.coord)
            self.cells[cL((oCell.coord[0],nCell.coord[1]))].removePiece()
            return True
        return False

    def validMoveB(self, oCell, nCell):
        if not (abs(oCell.coord[0]-nCell.coord[0])==abs(oCell.coord[1]-nCell.coord[1])):
            return False
        if (oCell.coord[0]>nCell.coord[0]):
            pnR = -1
        else:
            pnR = 1
        if (oCell.coord[1]>nCell.coord[1]):
            pnC = -1
        else:
            pnC = 1
        for i in range(1,abs(oCell.coord[0]-nCell.coord[0])):
            if self.cells[cL((oCell.coord[0]+i*pnR, \
                              oCell.coord[1]+i*pnC))].piece != 'none':
                return False
        return True
    def validMoveR(self, oCell, nCell):
        if not ((oCell.coord[0]-nCell.coord[0]==0) or
                (oCell.coord[1]-nCell.coord[1]==0)):
            return False
        if (oCell.coord[0]-nCell.coord[0]==0):
            if oCell.coord[1]>nCell.coord[1]:
                pm = -1
            else:
                pm = 1
            for i in range(1, abs(oCell.coord[1]-nCell.coord[1])):
                if self.cells[cL((oCell.coord[0],oCell.coord[1]+i*pm))].piece != 'none':
                    return False
        else:
            if oCell.coord[0]>nCell.coord[0]:
                pm = -1
            else:
                pm = 1
            for i in range(1, abs(oCell.coord[0]-nCell.coord[0])):
                if self.cells[cL((oCell.coord[0]+i*pm,oCell.coord[1]))].piece != 'none':
                    return False
        return True

    def validMoveQ(self, oCell, nCell):
        return self.validMoveR(oCell, nCell) or self.validMoveB(oCell, nCell)

    def update_pState(self):
        if self.turn == 0:
            let = 'b'
        else:
            let = 'w'
        for i in range(len(self.cells)):
            if self.cells[i].piece[0]==let:
                if self.cells[i].firstMoveOver=='current':
                    self.cells[i].firstMoveOver='finished'

    def toFINISHED(self,coord):
        self.cells[cL(coord)].firstMoveOver=='finished'

    def toCURRENT(self,coord):
        if self.cells[cL(coord)].firstMoveOver=='NA':
            self.cells[cL(coord)].firstMoveOver='current'

        
def play_chess():
    root = Tk()
    root.title('Chess')
    game = chessBoard(root)
    root.mainloop()
play_chess()
