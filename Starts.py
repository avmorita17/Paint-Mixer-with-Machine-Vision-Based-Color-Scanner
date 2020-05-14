import cv2 as cv2
import imutils
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font

import PIL
from PIL import Image
from PIL import ImageTk
import serial
import numpy as np
import time
import re
import os
import datetime

SerialData = serial.Serial('/dev/ttyACM0', 9600, timeout = 0.2)
time.sleep(2)
SerialData.write(bytes("1", "utf-8"))
x = SerialData.read().decode("utf-8")
while (x != '0'):
    x = SerialData.read().decode("utf-8")
    print(x)

White = np.array([255, 255, 255])
Silver = np.array([191, 191, 191])
Gray = np.array([127, 127, 127])
Black = np.array([0, 0, 0])
Red = np.array([0, 0, 255])
Maroon = np.array([0, 0, 127])
Yellow = np.array([0, 255, 255])
Olive = np.array([0, 127, 127])
Lime = np.array([0, 255, 0])
Green = np.array([0, 127, 0])
Aqua = np.array([255, 255, 0])
Teal = np.array([127, 127, 0])
Blue = np.array([255, 0, 0])
Navy = np.array([127, 0, 0])
Fushia = np.array([255, 0, 255])
Purple = np.array([127, 0, 127])
lists = [White, Silver, Gray, Black, Red, Maroon,
             Yellow, Olive, Lime, Green, Aqua, Teal, Blue,
             Navy, Fushia, Purple]
Colorlist = ['White', 'Silver', 'Gray', 'Black', 'Red', 'Maroon',
             'Yellow', 'Olive', 'Lime', 'Green', 'Aqua', 'Teal', 'Blue',
             'Navy', 'Fushia', 'Purple']

def rgb2ryb(R, G, B):

        R = R/255
        G = G/255
        B = B/255
        
        I = min(R,G,B)

        r = R - I
        g = G - I
        b = B - I

        
        red = r - min(r,g)
        yellow = (g + min(r,g))/2
        blue = (b + g - min(r,g))/2
        try:
                n = (max(red,yellow,blue))/(max(r,g,b))
                redn = red/n
                yellown = yellow/n
                bluen = blue/n
        except:
                redn = 0
                yellown = 0
                bluen = 0

        I = min(1 - R ,1 - G, 1 - B)

        
        Redn = redn + I
        Yellown = yellown + I
        Bluen = bluen + I
        White = 3*(min(1-Redn,1-Yellown,1-Bluen))
        sums = Redn + Yellown + Bluen + White

        Red = (Redn/sums)*100
        Yellow = (Yellown/sums)*100
        Blue = (Bluen/sums)*100
        White = (White/sums)*100
        blk = 0
        
        if (Red > 28 and Yellow > 28 and Blue > 28):
                blk = Redn + Yellown + Bluen
                Red = 0
                Yellow = 0
                Blue = 0
                White = 3*(max(R,G,B))
                sums = blk + White
                blk = (blk/sums)*100
                White = (White/sums)*100
                
        return Red, Yellow, Blue, White, blk


def tkShow(Image_Input):
  nextButtonImg = Image.open(Image_Input)
  nextButtonImg = ImageTk.PhotoImage(nextButtonImg)
  return nextButtonImg

def detAveColor(Image_Input):
  myimg = cv2.imread(Image_Input)
  avg_color_per_row = np.average(myimg, axis=0)
  avg_color = np.average(avg_color_per_row, axis=0)
  blue = int(avg_color[0])
  green = int(avg_color[1])
  red = int(avg_color[2])
  return blue, green, red

def detColorName(blue, green, red):
  global lists
  previous = 0
  colorNumberInc = 0
  colorNumber = 0
  for compare in lists:
    color = np.array([blue, green, red])
    accuracy = detColorAccuracy(blue, green, red, compare[0], compare[1], compare[2])
    if accuracy > previous:
        previous = accuracy
        colorNumber = colorNumberInc
    colorNumberInc = colorNumberInc + 1
  return Colorlist[colorNumber]
    
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def detColorAccuracy(blue1, green1, red1, blue2, green2, red2):
  blue = (abs(blue1 - blue2))/blue1
  green = (abs(green1 -green2))/green1
  red = (abs(red1 - red2))/red1

  error = (blue + green + red)/3
  accuracy = 1 - error
  return accuracy

def GetPercentages():
    SerialData.write(bytes("A", "utf-8"))
    time.sleep(1)
    x = SerialData.readline().decode("utf-8")
    
    Reds = GetINFO(x,"AAA","BBB")
    Blues = GetINFO(x,"BBB","CCC")
    Yellows = GetINFO(x,"CCC","DDD")
    Blacks = GetINFO(x,"DDD","EEE")
    Whites = GetINFO(x,"EEE","FFF")

    if float(Reds) < 0:
        Reds = "0"
    if float(Blues) < 0:
        Blues = "0"
    if float(Yellows) < 0:
        Yellows = "0"
    if float(Blacks) < 0:
        Blacks = "0"
    if float(Whites) < 0:
        Whites = "0"
    if float(Reds) > 100:
        Reds = "100"
    if float(Blues) > 100:
        Blues = "100"
    if float(Yellows) > 100:
        Yellows = "100"
    if float(Blacks) > 100:
        Blacks = "100"
    if float(Whites) > 100:
        Whites = "100"
    text = ("Red: " + Reds + "%                  \nBlue: " + Blues + "%\nYellow: " + Yellows +
            "%\nBlack: " + Blacks + "%\nWhite: " + Whites + "%")
    tk.messagebox.showinfo('Ink', text)

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=240, height=340, bg='white')

def Mix():
    result = tk.messagebox.askquestion("Mix", "Are You Sure?", icon='warning')
    if result == 'yes':
        x = 1
        ret, capt=cap1.read()
        capt = imutils.resize(capt, width = 220)
        xxx = (str(datetime.datetime.now().strftime("%Y")) + str(datetime.datetime.now().strftime("%m")) + str(datetime.datetime.now().strftime("%d")) + str(datetime.datetime.now().strftime("%H")) + str(datetime.datetime.now().strftime("%M")) + str(datetime.datetime.now().strftime("%S")) + str(datetime.datetime.now().strftime("%f")))
        cv2.imwrite(('Database/'+xxx+'.jpg'),capt)
        while (x == 1):
            result2 = tk.messagebox.askquestion("Mix", "Mix Again?", icon='warning')
            if result2 == 'yes':
                x = 1
            else:
                x = 0
        try:
            PastPlace.place_forget()
        except:
            pass
    else:
        pass

def Mix1():
    result = tk.messagebox.askquestion("Mix", "Are You Sure?", icon='warning')
    if result == 'yes':
        x = 1
        while (x == 1):
            result2 = tk.messagebox.askquestion("Mix", "Mix Again?", icon='warning')
            if result2 == 'yes':
                x = 1
            else:
                x = 0
        try:
            PastPlace.place_forget()
        except:
            pass
    else:
        pass

def MixPast():
    global canvas
    global PastPlace
    PastPlace = tk.Frame(root, bg='white')
    PastPlace.place(x=0,y=0)
    
    Background = tk.Label(PastPlace, text='', bg='white')
    Background.pack()
    tkShow1(Background, "bg.png", 1)

    pack5 =  tk.Frame(PastPlace, bg='white')
    pack5.place(x=263,y=0)

    Label8 = tk.Label(pack5, text = "Please choose an image. ", font = subFont1, bg='white')
    Label8.pack()

    myframe=tk.Frame(pack5, width=240, height=340,relief=tk.GROOVE,bd=1, bg='white')
    myframe.pack()

    canvas=tk.Canvas(myframe)       
    frame=tk.Frame(canvas, bg='white')  #The frame for the list(the texts themselves)
    myscrollbar=tk.Scrollbar(myframe,orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set, bg='white')

    myscrollbar.pack(side="right",fill="y")
    canvas.pack(side="left")
    canvas.create_window((0,0),window=frame,anchor='nw')
    frame.bind("<Configure>", myfunction)

    Buttons9 = tk.Button(pack5, text = "BACK", font = subFont2, bg='white', command = Back)
    Buttons9.pack(padx=10, pady=10)
    
    PastImagesList = sorted(os.listdir('Database'))
    print(PastImagesList)
    Rows = len(PastImagesList)
    print(Rows)
    for i in range(Rows):
        print(i)
        Button6 = tk.Button(frame, font = subFont2, bg='white', command = Mix1)
        Button6.grid(row=i,column=1, padx=10, pady=3)
        CurrentImage = PastImagesList[i]
        CurrentImage = 'Database/' + CurrentImage
        tkShow1(Button6,CurrentImage,1)


    
def Clean():
    result = tk.messagebox.askquestion("Clean", "Are You Sure?", icon='warning')
    if result == 'yes':
        x = 1
        while (x == 1):
            result2 = tk.messagebox.askquestion("Clean", "Clean Again?", icon='warning')
            if result2 == 'yes':
                x = 1
            else:
                x = 0
        pass
    else:
        pass

def Close():
    quit()

def Back():
    print("Back")
    PastPlace.place_forget()

def GetINFO(Info, Header1, Header2):
  Output=''
  try:
    Info = re.search(Header1 + '(.+?)' + Header2, Info)
    if Info:
      Output = str(Info.group(1))
    if Output=='':
      Output=' '
  except:
    Output = ''
  return Output

def tkShow1(Label, Image_Input, Percentage):
  Img = cv2.imread(Image_Input)
  h,w = Img.shape[:2]
  h = int(h*Percentage)
  Img = imutils.resize(Img, height=h)
  cv2.imwrite("IMGSome.jpg", Img)
  nextButtonImg = Image.open("IMGSome.jpg")
  nextButtonImg = ImageTk.PhotoImage(nextButtonImg)
  Label.configure(image=nextButtonImg)
  Label.image = nextButtonImg
  return nextButtonImg

root=tk.Tk()    #Main Root
root.attributes('-zoomed', True)
root.configure(background='white')
subFont1 = tkinter.font.Font(family='Segoe UI', size = 15, weight = "bold")
subFont2 = tkinter.font.Font(family='Segoe UI', size = 10, weight = "bold")

cap1=cv2.VideoCapture(0)
cap2=cv2.VideoCapture(1)
    
def starts():
    global R
    global Y
    global B
    global W
    global blk
    ret, capt1 = cap1.read()
    capt1 = imutils.resize(capt1, width = 220)
    cv2.imwrite("capt1.jpg", capt1)
    
    capt1 = tkShow("capt1.jpg")

    blue1, green1, red1 = detAveColor("capt1.jpg")
    
    Color = detColorName(blue1, green1, red1)

    R,Y,B,W,blk = rgb2ryb(red1, green1, blue1)
    R = round(R, 2)
    Y = round(Y, 2)
    B = round(B, 2)
    W = round(W, 2)
    blk = round(blk, 2)
    Label7.configure(text = ("Red: " + str(R) + "% Yellow: " + str(Y) + "% Blue: " + str(B) + "% White:" + str(W) + "% Black: " + str(blk) + "%"))

    Image1.configure(image=capt1)
    Image1.image = capt1

    ret, capt2 = cap2.read()
    capt2 = imutils.resize(capt2, width = 220)
    cv2.imwrite("capt2.jpg", capt2)
    
    capt2 = tkShow("capt2.jpg")

    blue2, green2, red2 = detAveColor("capt2.jpg")

    error = detColorAccuracy(blue1, green1, red1, blue2, green2, red2)  

    Label3a.configure(text=("     Blue: " + str(blue1)))
    Label3b.configure(text=("     Blue: " + str(blue2)))

    Label4a.configure(text=("     Green: " + str(green1)))
    Label4b.configure(text=("     Green: " + str(green2)))

    Label5a.configure(text=("     Red: " + str(red1)))
    Label5b.configure(text=("     Red: " + str(red2)))

    error = round(error*100, 2)
    
    Label6.configure(text = ("Accuracy: " + str(error)))
    
    Image2.configure(image=capt2)
    Image2.image = capt2    
    root.after(5,starts)


pack1 =  tk.Frame(root, bg='white')
pack1.pack(side=tk.TOP, anchor=tk.CENTER)

Image1 = tk.Label(pack1, text = "", bg='white')
Image1.grid(row=1,column=1, padx=10, pady=5)

Label1a = tk.Label(pack1, text = "INPUT", font = subFont1, bg='white')
Label1a.grid(row=2,column=1, padx=10, pady=5)

Label2a = tk.Label(pack1, text = "   Average Color: ", font = subFont2, bg='white')
Label2a.grid(row=3,column=1, padx=10, pady=3, sticky = tk.W)

Label3a = tk.Label(pack1, text = "     Blue: ", font = subFont2, bg='white')
Label3a.grid(row=4,column=1, padx=10, pady=3, sticky = tk.W)

Label4a = tk.Label(pack1, text = "     Green: ", font = subFont2, bg='white')
Label4a.grid(row=5,column=1, padx=10, pady=3, sticky = tk.W)

Label5a = tk.Label(pack1, text = "     Red: ", font = subFont2, bg='white')
Label5a.grid(row=6,column=1, padx=10, pady=3, sticky = tk.W)

Image2 = tk.Label(pack1, text = "", bg='white')
Image2.grid(row=1,column=2, padx=10, pady=10)

Label2a = tk.Label(pack1, text = "OUTPUT", font = subFont1, bg='white')
Label2a.grid(row=2,column=2, padx=10, pady=5)

Label2b = tk.Label(pack1, text = "   Average Color: ", font = subFont2, bg='white')
Label2b.grid(row=3,column=2, padx=10, pady=3, sticky = tk.W)

Label3b = tk.Label(pack1, text = "     Blue: ", font = subFont2, bg='white')
Label3b.grid(row=4,column=2, padx=10, pady=3, sticky = tk.W)

Label4b = tk.Label(pack1, text = "     Green: ", font = subFont2, bg='white')
Label4b.grid(row=5,column=2, padx=10, pady=3, sticky = tk.W)

Label5b = tk.Label(pack1, text = "     Red: ", font = subFont2, bg='white')
Label5b.grid(row=6,column=2, padx=10, pady=3, sticky = tk.W)

pack2 =  tk.Frame(root, bg='white')
pack2.pack(side=tk.TOP, anchor=tk.CENTER)

Label6 = tk.Label(pack2, text = "Accuracy: ", font = subFont2, bg='white')
Label6.grid(row=1,column=1, padx=10, pady=3)

pack3 =  tk.Frame(root, bg='white')
pack3.pack(side=tk.TOP, anchor=tk.CENTER)

Button1 = tk.Button(pack3, text = "Check Paint Levels", font = subFont2, bg='white', command = GetPercentages)
Button1.grid(row=1,column=1, padx=10, pady=3)

Button2 = tk.Button(pack3, text = "Mix!", font = subFont2, bg='white', command = Mix)
Button2.grid(row=1,column=2, padx=10, pady=3)

Button3 = tk.Button(pack3, text = "Mix Past Samples", font = subFont2, bg='white', command = MixPast)
Button3.grid(row=1,column=3, padx=10, pady=3)

Button4 = tk.Button(pack3, text = "Clean Tubes", font = subFont2, bg='white', command = Clean)
Button4.grid(row=1,column=4, padx=10, pady=3)

Button5 = tk.Button(pack3, text = "Close", font = subFont2, bg='white', command = Close)
Button5.grid(row=1,column=5, padx=10, pady=3)

pack4 =  tk.Frame(root, bg='white')
pack4.pack(side=tk.TOP, anchor=tk.CENTER)

Label7 = tk.Label(pack4, font = subFont2, bg='white')
Label7.grid(row=1,column=1, padx=10, pady=3) 

root.after(5,starts)
root.mainloop()
