#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 16:39:08 2022

@author: MateP
"""

from tkinter import Tk, Frame, Checkbutton, BooleanVar, Scale, HORIZONTAL, Label
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

N = 100


def InvLLike(a, b, c, d, e):
    return lambda x, y: (y/b, x-1+a*abs(y)/b)


class Loziclass(object):
    """docstring for Loziclass."""

    def __init__(self, a=1, b=.5):
        super(Loziclass, self).__init__()
        self.update(a, b)

    def update(self, a, b):
        self.a = a
        self.b = b
        self.X = np.array([1/(1+a-b), b/(1+a-b)])
        self.Y = np.array([1/(1-a-b), b/(1-a-b)])
        self.Xu = np.array([-a-np.sqrt(a**2+4*b), 2*b])
        self.Xs = np.array([-a+np.sqrt(a**2+4*b), 2*b])
        self.Yu = np.array([a+np.sqrt(a**2+4*b), 2*b])
        self.Ys = np.array([a-np.sqrt(a**2+4*b), 2*b])

    def L(self, pt):
        x, y = pt
        return np.array([1-self.a*abs(x)+y, self.b*x])

    def LI(self, pt):
        x, y = pt
        return np.array([y/self.b, x-1+self.a*abs(y/self.b)])

    def extend(self, pts, rev, forward, N):
        counter = 1
        while len(pts) < N:

            if rev:
                pts.reverse()

            newcounter = 0

            while counter > 0:
                counter -= 1

                current = pts[-1]
                if rev:
                    index = counter
                else:
                    index = -1-counter-newcounter
                if forward:
                    tmp = self.L(pts[index])
                    k = 0
                else:
                    tmp = self.LI(pts[index])
                    k = 1

                if tmp[k]*current[k] < 0:
                    t = -current[k]/(tmp[k]-current[k])
                    new = current+t*(tmp-current)
                    pts.append(new)
                    newcounter += 1
                pts.append(tmp)
                newcounter += 1

            counter = newcounter

    def unstableX(self):
        pts = [self.X]
        t = -self.X[0]/self.Xu[0]

        pts.append(self.X+t*self.Xu)
        self.extend(pts, rev=True, forward=True, N=N)

        tmp = np.array(pts).T

        tmp2 = tmp[1][(tmp[0] < 3) & (tmp[0] > -3)]
        self.maxy = tmp2.max()
        self.miny = tmp2.min()

        return tmp

    def stableX(self):
        pts = [self.X]
        t = -self.X[1]/self.Xs[1]

        pts.insert(0, self.X-10*t*self.Xs)
        pts.append(self.X+t*self.Xs)
        self.extend(pts, rev=False, forward=False, N=N)
        return np.array(pts).T

    def unstableY(self):
        pts = [self.Y]
        t = -self.Y[0]/self.Yu[0]

        pts.insert(0, self.Y-10*t*self.Yu)
        pts.append(self.Y+t*self.Yu)
        self.extend(pts, rev=False, forward=True, N=N)
        return np.array(pts).T

    def stableY(self):
        pts = [self.Y]
        t = -self.Y[1]/self.Ys[1]

        pts.append(self.Y+t*self.Ys)
        self.extend(pts, rev=True, forward=False, N=N)
        return np.array(pts).T


def main():
    root = Tk()
    root.wm_title("Lozi map")

    Lozi = Loziclass()

    frame1 = Frame(root)
    figure1 = Figure()
    ax1 = figure1.add_subplot()
    canvas1 = FigureCanvasTkAgg(figure1, frame1)

    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)
    ax1.grid()
    ax1.set(xlabel='x', ylabel='y')

    X, = ax1.plot(*Lozi.X, 'ro')
    Y, = ax1.plot(*Lozi.Y, 'go')

    unstableX, = ax1.plot(*Lozi.unstableX())
    unstableY, = ax1.plot(*Lozi.unstableY())
    stableX, = ax1.plot(*Lozi.stableX())
    stableY, = ax1.plot(*Lozi.stableY())

    frame2 = Frame(root)
    figure2 = Figure()
    ax2 = figure2.add_subplot()

    def updateVisibility():
        unstableX.set_visible(uXcheck.get())
        stableX.set_visible(sXcheck.get())
        unstableY.set_visible(uYcheck.get())
        stableY.set_visible(sYcheck.get())
        canvas1.draw()

    def updateScale():
        if autoScaleCheck.get():
            ax1.set_ylim(Lozi.miny, Lozi.maxy)
        else:
            ax1.set_ylim(-3, 3)

        canvas1.draw()

    def getorigin(eventorigin):
        if eventorigin.widget == canvas2.get_tk_widget():
            x = eventorigin.x
            y = eventorigin.y
            a, b = ax2.transData.inverted().transform([x, y])
            b = ax2.get_ylim()[1]-b
            dot2.set_data([a, b])

            Lozi.update(a, b)

            aLabel['text'] = f'a={Lozi.a:.10f}'
            bLabel['text'] = f'b={Lozi.b:.10f}'

        X.set_data(Lozi.X)
        Y.set_data(Lozi.Y)

        unstableX.set_data(*Lozi.unstableX())
        stableX.set_data(*Lozi.stableX())
        unstableY.set_data(*Lozi.unstableY())
        stableY.set_data(*Lozi.stableY())

        if autoScaleCheck.get():
            ax1.set_ylim(Lozi.miny, Lozi.maxy)

        canvas1.draw()
        canvas2.draw()

    def changeN(n):
        global N
        N = int(n)
        unstableX.set_data(*Lozi.unstableX())
        stableX.set_data(*Lozi.stableX())
        unstableY.set_data(*Lozi.unstableY())
        stableY.set_data(*Lozi.stableY())

        canvas1.draw()
        canvas2.draw()

    uXcheck = BooleanVar(value=True)
    sXcheck = BooleanVar(value=True)
    uYcheck = BooleanVar(value=True)
    sYcheck = BooleanVar(value=True)
    autoScaleCheck = BooleanVar(value=False)

    aLabel = Label(frame2, text=f'a={Lozi.a:.10f}')

    bLabel = Label(frame2, text=f'b={Lozi.b:.10f}')

    L1 = Label(frame2, text="How many points (N)")

    Nscale = Scale(frame2, tickinterval=50, length=500, from_=0,
                   to=500, orient=HORIZONTAL, command=changeN)
    Nscale.set(50)

    C1 = Checkbutton(frame2, text='unstable X',
                     command=updateVisibility, variable=uXcheck)

    C2 = Checkbutton(frame2, text='stable X',
                     command=updateVisibility, variable=sXcheck)

    C3 = Checkbutton(frame2, text='unstable Y',
                     command=updateVisibility, variable=uYcheck)

    C4 = Checkbutton(frame2, text='stable Y',
                     command=updateVisibility, variable=sYcheck)

    C5 = Checkbutton(frame2, text='autoscale',
                     command=updateScale, variable=autoScaleCheck)

    canvas2 = FigureCanvasTkAgg(figure2, frame2)

    ax2.set_xlim(0, 3)
    ax2.set_ylim(0, 1)
    ax2.grid()
    ax2.set(xlabel='a', ylabel='b')
    dot2, = ax2.plot(1, .5, 'ro')

    x = np.linspace(0, 3, 103)
    ax2.plot(x, abs(x-1))
    ax2.plot(x, np.sqrt(2)*x-2)
    ax2.plot(x, (x**2-1)/(2*x+1))
    ax2.plot(x, 4-2*x)

    y = np.linspace(0, 1, 103)
    ax2.plot((1+y+3*np.sqrt(1+y**2))/2, y)
    ax2.plot(np.sqrt(3*y**2+4+np.sqrt((3*y**2+4)**2-32*y**3))/2, y)

    def redraw(event=None):
        screen_width = root.winfo_width()
        px_scale = int(9*screen_width/16)
        screen_height = px_scale

        frame1.place(x=0, y=0, width=screen_height, height=screen_height)
        canvas1.get_tk_widget().place(x=0, y=0, width=screen_height, height=screen_height)
        frame2.place(x=screen_height, y=0, width=screen_width -
                     screen_height, height=screen_height)
        aLabel.place(x=int(px_scale*.5), y=int(px_scale*.45))
        bLabel.place(x=int(px_scale*.5), y=int(px_scale*.5))
        L1.place(x=int(px_scale*.03), y=int(px_scale*.1))
        Nscale.place(x=int(px_scale*.03), y=int(px_scale*.15))
        C1.place(x=int(px_scale*.03), y=int(px_scale*.3))
        C2.place(x=int(px_scale*.03), y=int(px_scale*.35))
        C3.place(x=int(px_scale*.03), y=int(px_scale*.4))
        C4.place(x=int(px_scale*.03), y=int(px_scale*.45))
        C5.place(x=int(px_scale*.03), y=int(px_scale*.05))
        canvas2.get_tk_widget().place(x=int(px_scale*.02), y=int(px_scale*.55),
                                      width=int(px_scale*.75), height=int(px_scale*.4))

    px_scale = 720
    screen_width = int(16*px_scale/9)
    screen_height = px_scale

    root.geometry(f'{screen_width}x{screen_height}+0+0')

    redraw()

    root.bind("<Configure>", redraw)
    root.bind("<B1-Motion>", getorigin)
    root.bind("<Button-1>", getorigin)

    root.bind("<Escape>", lambda event: root.destroy())

    root.mainloop()


if __name__ == "__main__":
    main()
