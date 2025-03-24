#Version 2.5
import pyautogui as Pg
import time as T
import pynput as put

# [edit1] all variable in type any 
re_running = False # [edit-1] I don't remember what propost of this variable
running = True
Start = False
mouse = put.mouse.Controller() 
AllowToStop = True # this for check if can I stop now (use in keyboard listener)

def Countdown(Ti): # [edit2] argument type any
    while Ti and Start:
        mins, secs = divmod(Ti , 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        T.sleep(1)
        Ti-= 1

def Pgcoast_choose():
    choose = input("receive or click(r/c/r2/r3 (date) : ")

    if choose == 'r':
        receive_event()
    elif choose == 'c':
        click_event()
    elif choose == "r2":
        receive_event_2()
    elif choose == "r3":
        receive_event_3()
    else:
        print("r and c and r2 and r3 only")
        Pgcoast_choose()



def click_event():
    CT = int(input("CD(sec) :"))
    print("press 1 to start")
    global AllowToStop
    AllowToStop = True

    while running:
        X = [233,846,930,889,1806]
        Y = [1051,783,680,722,16]

        if Start:
            Pg.moveTo(X[0],Y[0], duration = 0.2)
            Pg.click()

            Pg.moveTo(X[1],Y[1], duration=0.2)

            Click_count = (CT/60)+2

            while not Click_count <0:
                if Start == False:
                    break
                Pg.click()
                T.sleep(0.5)
                Click_count -= 1
                
            T.sleep(2)

            Count = 2
            while Count < 5:
                if Start == False:
                    break 
                Pg.moveTo(X[Count],Y[Count], duration = 0.2)
                Pg.click()
                T.sleep(1)
                Count += 1

            if Start:
                Countdown(CT-1)

def receive_event_2():
    
    global re_running, AllowToStop
    AllowToStop = True
    re_running = True
    CT= int(input("CD(sec) :"))
    print("press 1 to start")

    while running:
        X=[269,743,1117,956,946,1811]
        Y=[1064,885,803,732,941,24]
        LenX= len(X)

        if Start:
            for i in range(LenX):
                if Start == False:
                    break

                Pg.moveTo(X[i],Y[i],duration = 0.2)
                Pg.click(X[i],Y[i])
                T.sleep(1)
            if Start:
                Countdown(CT-1)

def receive_event_3():
    
    global re_running, AllowToStop
    AllowToStop = True
    re_running = True
    CT= int(input("CD(sec) :"))
    print("press 1 to start")

    while running:
        X=[269,1077,731,1117,956,946,719,1795]
        Y=[1064,864,711,803,732,943,985,5]
        LenX= len(X)

        if Start:
            for i in range(LenX):
                if Start == False:
                    break

                Pg.moveTo(X[i],Y[i],duration = 0.2)
                Pg.click(X[i],Y[i])
                T.sleep(1)
            if Start:
                Countdown(CT-1)


def receive_event():
    
    global re_running, AllowToStop
    AllowToStop = True
    re_running = True
    CT= int(input("CD(sec) :"))
    print("press 1 to start")

    while running:
        X=[269,940,731,1117,956,946,719,1795]
        Y=[1064,576,819,803,732,943,985,5]
        LenX= len(X)

        if Start:
            for i in range(LenX):
                if Start == False:
                    break

                Pg.moveTo(X[i],Y[i],duration = 0.2)
                Pg.click(X[i],Y[i])
                T.sleep(1)
            if Start:
                Countdown(CT-1)

def PgsetM():
    
    CT= int(input("CD(sec) :"))

    X = []
    Y = []
    while True:
        SW = input("save or enough(s/e/p)\n")
        if SW == 's':
            T.sleep(3)
            curX,curY = Pg.position()
            X.append(curX)
            Y.append(curY)
            print(X,Y)
        elif SW == 'p':
            X.pop()
            Y.pop()
            print(X,Y)
        elif SW == 'e':
            break
        else:
            print("not have this key")

    print("x = ",X,"and Y =",Y)
    global AllowToStop
    AllowToStop = True
    LenX = len(X)
    print("press 1 to start")

    while running:
        if Start:
            for i in range(LenX):
                if Start == False:
                    break
                Pg.moveTo(X[i],Y[i],duration = 0.2)
                Pg.click(X[i],Y[i])
                T.sleep(1)
            if Start:
                Countdown(CT-1)


def bot_start():
        
        global re_running, running, AllowToStop
        AllowToStop = False
        running = True
        Option = int(input("2.ตำแหน่งคงที่ 3.เซฟตำแหน่ง(2/3)\n"))

        if Option == 2:
            Pgcoast_choose()
        elif Option == 3:
            PgsetM()
        else:
            print("2 and 3 only")

        
def toggle_event(key):
    if key == put.keyboard.KeyCode(char='1'):
        global Start
        Start = not Start
        print(Start, end= ("\r"))
    elif key == put.keyboard.Key.esc and AllowToStop == True:
        print("stop working")
        global running 
        running = False
        Start = False
        return False
    elif key == put.keyboard.KeyCode(char='4'):
        running = False
        Start = False
        bot_start()


Li = put.keyboard.Listener (on_press=toggle_event) 
Li.start()

bot_start()