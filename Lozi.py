#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 16:39:08 2022

@author: mate
"""

from tkinter import Tk,Frame, Checkbutton, BooleanVar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

N=1000

def InvLLike(a,b,c,d,e):
    return lambda x,y: (y/b,x-1+a*abs(y)/b)


class Loziclass(object):
    """docstring for Loziclass."""

    def __init__(self, a=1,b=.5):
        super(Loziclass, self).__init__()
        self.update(a,b)
        
    def update(self,a,b):
        self.a=a
        self.b=b
        self.X = np.array([1/(1+a-b),b/(1+a-b)])
        self.Y = np.array([1/(1-a-b),b/(1-a-b)])
        self.Xu = np.array([-a-np.sqrt(a**2+4*b),2*b])
        self.Xs = np.array([-a+np.sqrt(a**2+4*b),2*b])
        self.Yu = np.array([a+np.sqrt(a**2+4*b),2*b])
        self.Ys = np.array([a-np.sqrt(a**2+4*b),2*b])
        
    def L(self,pt):
        x,y=pt
        return np.array([1-self.a*abs(x)+y, self.b*x])
    
    def LI(self,pt):
        x,y=pt
        return np.array([y/self.b, x-1+self.a*abs(y/self.b)])
    
    def extend(self,pts,rev,forward,N):
        counter=1
        while len(pts)<N:
            
            if rev:
                pts.reverse()
                
            newcounter=0
            
            while counter>0:
                counter-=1
                
                
                current = pts[-1]
                if rev:
                    index=counter
                else:
                    index=-1-counter-newcounter
                if forward:
                    tmp=self.L(pts[index])
                    k=0
                else:
                    tmp=self.LI(pts[index])
                    k=1
                    
                if tmp[k]*current[k]<0:
                    t=-current[k]/(tmp[k]-current[k])
                    new = current+t*(tmp-current)
                    pts.append(new)
                    newcounter+=1
                pts.append(tmp)
                newcounter+=1
                
            counter = newcounter
            
        
        
    def unstableX(self):
        pts=[self.X]
        t=-self.X[0]/self.Xu[0]
        
        pts.append(self.X+t*self.Xu)
        self.extend(pts,rev=True,forward=True,N=N)
        return np.array(pts).T
    
    def stableX(self):
        pts=[self.X]
        t=-self.X[1]/self.Xs[1]
        
        pts.insert(0, self.X-10*t*self.Xs)
        pts.append(self.X+t*self.Xs)
        self.extend(pts,rev=False,forward=False,N=N)
        return np.array(pts).T
    
    def unstableY(self):
        pts=[self.Y]
        t=-self.Y[0]/self.Yu[0]
        
        pts.insert(0, self.Y-10*t*self.Yu)
        pts.append(self.Y+t*self.Yu)
        self.extend(pts,rev=False,forward=True,N=N)
        return np.array(pts).T
    
    def stableY(self):
        pts=[self.Y]
        t=-self.Y[1]/self.Ys[1]
        
        pts.append(self.Y+t*self.Ys)
        self.extend(pts,rev=True,forward=False,N=N)
        return np.array(pts).T
        
    


def main():
    root = Tk()
    root.wm_title("Lozi map")
    root.geometry('1280x720+1280+0')
    
    
    Lozi=Loziclass()
    
    frame1 = Frame(root);
    figure1, ax1 = plt.subplots()

    frame1.place(x=0, y=0, width=720, height=720)

    canvas1 = FigureCanvasTkAgg(figure1, frame1)
    canvas1.get_tk_widget().place(x=0,y=0,width=720,height=720)

    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)
    ax1.grid()
    ax1.set(xlabel='x', ylabel='y')
    
    X, = ax1.plot(*Lozi.X,'ro')
    Y, = ax1.plot(*Lozi.Y,'go')

    
    
    unstableX, = ax1.plot(*Lozi.unstableX())
    unstableY, = ax1.plot(*Lozi.unstableY())
    stableX, = ax1.plot(*Lozi.stableX())
    stableY, = ax1.plot(*Lozi.stableY())

    frame2 = Frame(root);
    figure2, ax2 = plt.subplots()

    frame2.place(x=720, y=0, width=560, height=720)
    
    def updateVisibility():
        unstableX.set_visible(uXcheck.get())
        stableX.set_visible(sXcheck.get())
        unstableY.set_visible(uYcheck.get())
        stableY.set_visible(sYcheck.get())
        canvas1.draw()
        
        
        
    uXcheck = BooleanVar(value=True)
    sXcheck = BooleanVar(value=True)
    uYcheck = BooleanVar(value=True)
    sYcheck = BooleanVar(value=True)
    
    Checkbutton(frame2, text='unstable X',command=updateVisibility, variable=uXcheck).place(x=20,y=300)
    Checkbutton(frame2,text='stable X',command=updateVisibility, variable=sXcheck).place(x=20,y=320)
    Checkbutton(frame2,text='unstable Y',command=updateVisibility, variable=uYcheck).place(x=20,y=340)
    Checkbutton(frame2,text='stable Y',command=updateVisibility, variable=sYcheck).place(x=20,y=360)

    canvas2 = FigureCanvasTkAgg(figure2, frame2)
    canvas2.get_tk_widget().place(x=10,y=400,width=540,height=280)

    ax2.set_xlim(0, 3)
    ax2.set_ylim(0, 1)
    ax2.grid()
    ax2.set(xlabel='a', ylabel='b')
    dot2, = ax2.plot(.5,.5,'ro')


    def getorigin(eventorigin):
        if eventorigin.widget == canvas2.get_tk_widget():
            x = eventorigin.x
            y = eventorigin.y
            a,b = ax2.transData.inverted().transform([x,y])
            b=ax2.get_ylim()[1]-b

            Lozi.update(a,b)
            
            

            X.set_data(Lozi.X)
            Y.set_data(Lozi.Y)
            
            unstableX.set_data(*Lozi.unstableX())
            stableX.set_data(*Lozi.stableX())
            unstableY.set_data(*Lozi.unstableY())
            stableY.set_data(*Lozi.stableY())
            
            
            dot2.set_xdata([a,2])
            dot2.set_ydata([b,3])

            canvas1.draw()
            canvas2.draw()

    root.bind("<B1-Motion>",getorigin)
    root.bind("<Button-1>",getorigin)

    root.bind("<Escape>", lambda event: root.destroy())



    root.mainloop()

if __name__ == "__main__":
    main()
