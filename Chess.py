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
        self.x=coord[0]
        self.y=coord[1]
        self.f=f(self.x,self.y)
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
                if (self.master.validMove(  f(pieceClicked[1].x,pieceClicked[1].y), \
                                            f(self.x           ,self.y)            )):
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

    def validMove(self, oCell, nCell):
        ''' Given the starting cell (oCell) and the 
            ending cell (nCell), this function returns whether
            it is a valid move. 

            Function will be given index of the cells in the list \'self.cells\''''
        ############ Work in Progress #############
        return True

def play_chess():
    root = Tk()
    root.title('Chess')
    game = chessBoard(root)
    root.mainloop()


play_chess()
