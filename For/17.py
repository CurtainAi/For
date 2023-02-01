import tkinter as tk
from PIL import ImageTk, Image

win = tk.Tk()
pastRes = 0
lastOp = ""


def zero():
    temp = showNumber.get() * 10
    showNumber.set(temp)


def one():
    temp = showNumber.get() * 10 + 1
    showNumber.set(temp)


def two():
    temp = showNumber.get() * 10 + 2
    showNumber.set(temp)


def three():
    temp = showNumber.get() * 10 + 3
    showNumber.set(temp)


def four():
    temp = showNumber.get() * 10 + 4
    showNumber.set(temp)


def five():
    temp = showNumber.get() * 10 + 5
    showNumber.set(temp)


def six():
    temp = showNumber.get() * 10 + 6
    showNumber.set(temp)


def seven():
    temp = showNumber.get() * 10 + 7
    showNumber.set(temp)


def eight():
    temp = showNumber.get() * 10 + 8
    showNumber.set(temp)


def nine():
    temp = showNumber.get() * 10 + 9
    showNumber.set(temp)


def AC():
    global pastRes
    global lastOp
    showNumber.set(0)
    lastOp = ""
    pastRes = 0


def add():
    global lastOp
    global pastRes
    math()
    lastOp = "add"
    showNumber.set(0)


def sub():
    global lastOp
    global pastRes
    math()
    lastOp = "sub"
    showNumber.set(0)


def mul():
    global lastOp
    global pastRes
    math()
    lastOp = "mul"
    showNumber.set(0)


def div():
    global lastOp
    global pastRes
    math()
    lastOp = "div"
    showNumber.set(0)


def equal():
    global pastRes
    global lastOp
    math()
    showNumber.set(int(pastRes))
    lastOp = "equal"


def math():
    global pastRes
    if lastOp == "add":
        pastRes = pastRes + showNumber.get()
    elif lastOp == "sub":
        pastRes = pastRes - showNumber.get()
    elif lastOp == "mul":
        pastRes = pastRes * showNumber.get()
    elif lastOp == "div":
        pastRes = pastRes / showNumber.get()
    elif lastOp == "equal":
        pastRes = pastRes + 0
    elif lastOp == "":
        pastRes = showNumber.get()


win.wm_title("sgbyg")
win.resizable(width=False, height=False)
win.minsize(width=480, height=480)
win.maxsize(width=480, height=480)
x = Image.open("bg.png")
img = ImageTk.PhotoImage(x)
labelBackground = tk.Label(win, image=img)
labelBackground.pack()
labelDigits = tk.Label(win, text="12 Digits", fg="#537791", bg="#c1c0b9", bd=0, font=("Helvetica", 30))
labelDigits.place(x=60, y=100)
showNumber = tk.IntVar()
showNumber.set(0)
labelShow = tk.Label(win, text="", textvariable=showNumber, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50),
                     width=13)
labelShow.place(x=60, y=20)
btnZero = tk.Button(win, text="0", command=zero, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50), width=4)
btnZero.place(x=60, y=400)
btnOne = tk.Button(win, text="1", command=one, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50))
btnOne.place(x=60, y=320)
btnTwo = tk.Button(win, text="2", command=two, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50))
btnTwo.place(x=150, y=320)
btnThree = tk.Button(win, text="3", command=three, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50))
btnThree.place(x=240, y=320)
btnFour = tk.Button(win, text="4", command=four, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50))
btnFour.place(x=60, y=240)
btnFive = tk.Button(win, text="5", command=five, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50))
btnFive.place(x=150, y=240)
btnSix = tk.Button(win, text="6", command=six, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50))
btnSix.place(x=240, y=240)
btnSeven = tk.Button(win, text="7", command=seven, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50))
btnSeven.place(x=60, y=160)
btnEight = tk.Button(win, text="8", command=eight, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50))
btnEight.place(x=150, y=160)
btnNine = tk.Button(win, text="9", command=nine, fg="#c1c0b9", bg="#537791", bd=0, font=("Helvetica", 50))
btnNine.place(x=240, y=160)
btnEqual = tk.Button(win, text="=", command=equal, fg="#537791", bg="#537791", bd=0, font=("Helvetica", 50))
btnEqual.place(x=240, y=400)
btnAdd = tk.Button(win, text="+", command=add, fg="#537791", bg="#537791", bd=0, font=("Helvetica", 50), width=2)
btnAdd.place(x=330, y=160)
btnSub = tk.Button(win, text="–", command=sub, fg="#537791", bg="#537791", bd=0, font=("Helvetica", 50), width=2)
btnSub.place(x=330, y=240)
btnMul = tk.Button(win, text="&#10005;", command=mul, fg="#537791", bg="#537791", bd=0, font=("Helvetica", 50), width=2)
btnMul.place(x=330, y=320)
btnDiv = tk.Button(win, text="/", command=div, fg="#537791", bg="#537791", bd=0, font=("Helvetica", 50), width=2)
btnDiv.place(x=330, y=400)
btnClick = tk.Button(win, text="AC", command=AC, fg="#537791", bg="#537791", bd=0, font=("Helvetica", 40))
btnClick.place(x=329, y=100)
win.mainloop()