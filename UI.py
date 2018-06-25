import tkinter as tk
from Experiment1 import Experiment
from Experiment2 import ExperimentTwo
from Experiment3 import ExperimentThree
import random
import sys
import time
Width = 80
(x, y) = (5, 5)



def Draw():
    board = tk.Canvas(root, width=x * Width, height=y * Width)
    frame=tk.Frame(root)
    frame.grid(row=0,column=1)
    v = tk.IntVar()
    v1 =tk.IntVar()
    Experiment1 = Experiment(root,board)
    Experiment2 = ExperimentTwo(root, board)
    Experiment3 = ExperimentThree(root, board)
    button1=tk.Radiobutton(frame, text="Experiment1", variable=v, value=1,command=Experiment1.PRandom)
    button2=tk.Radiobutton(frame, text="Experiment2", variable=v, value=2,command=Experiment2.PRandom)
    button3 = tk.Radiobutton(frame, text="Experiement3", variable=v, value=3,command=Experiment3.PRandom)

    button1.grid(row=1,column=1)
    button2.grid(row=1,column=2)
    button3.grid(row=1,column=3)
    if v.get()==1:
        Experiment1.PRandom()
    if v.get()==2:
        Experiment2.PRandom()
    if v.get()==3:
        Experiment3.PRandom()

    root.mainloop()


root = tk.Tk()
Draw()

#PRandom()
