from tkinter import *
from PIL import ImageTk, Image

def f(x, y):
    return x*8+y

class Piece(Canvas):

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
        self.bgColor=BG
        self.x=coord[0]
        self.y=coord[1]
        self.f=f(self.x,self.y)
        self.slength=50
        Canvas.__init__(self,master,width=self.slength,height=self.slength,bg=self.bgColor,highlightthickness=0,relief=RAISED)

        self.piece='none'
        self.text = self.create_text(50/2,50/2,anchor = "center", text="", fill='black', font = ("Arial", 24))

        self.bind("<Button-1>",self.move)

    def createPiece(self,pieceName, size=(50,50)):
        self.itemconfig(self.text,text=pieceName[0:2])
        # self.createImage(pieceName,size)
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
        self.itemconfig(self.text,text="")

    def highlight(self):
        self['bg']='lightgreen'

    def unhighlight(self):
        self['bg']=self.bgColor

    def isHighlighted(self):
        return self['bg']=='lightgreen'

    def move(self, misc=''):
        if self.isHighlighted():
            self.unhighlight()
            return 0
        self.master.unhighlight()
        self.highlight()

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
        self.cells[1].createPiece('bknit')
        self.cells[2].createPiece('bbish')
        self.cells[3].createPiece('bquen')
        self.cells[4].createPiece('bking')
        self.cells[5].createPiece('bbish')
        self.cells[6].createPiece('bknit')
        self.cells[7].createPiece('brook')
        for i in range(8):
            self.cells[f(1,i)].createPiece('bpawn')
            self.cells[f(6,i)].createPiece('wpawn')
        self.cells[f(7,0)].createPiece('wrook')
        self.cells[f(7,1)].createPiece('wknit')
        self.cells[f(7,2)].createPiece('wbish')
        self.cells[f(7,3)].createPiece('wquen')
        self.cells[f(7,4)].createPiece('wking')
        self.cells[f(7,5)].createPiece('wbish')
        self.cells[f(7,6)].createPiece('wknit')
        self.cells[f(7,7)].createPiece('wrook')
        self.turn = 0

    def toggleTurn(self):
        self.update_pState()
        self.turn = (self.turn+1)%2

    def unhighlight(self):
        for i in self.cells:
            i.unhighlight()



def play_chess():
    root = Tk()
    root.title('Chess')
    game = chessBoard(root)
    root.mainloop()

play_chess()
