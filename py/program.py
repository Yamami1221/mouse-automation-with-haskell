import tkinter as tk
import os
import pynput as pp
import time as T
import threading as TH

class Program:

    #program constructure
    def __init__(self) -> None:

        self.working = False
        self.clicking = False
        self.__delay = 0.02
        self.km = False

        self.root = self.Window().root_getter()
        self.ss_button = self.SS_button(self)

        self.root.mainloop()

    #getter
    def delay_getter(self):
        return self.__delay

    #inner class
    #root window
    class Window:

        def __init__(self) -> None:
            self.__root = tk.Tk()
            self.__root.geometry("500x500")
            self.__root.title = "AutoClick_by_SKOT"
            self.__root.protocol("WM_DELETE_WINDOW",  self.on_close)
            self.__root.resizable(False, False)

        def root_getter(self):
            return self.__root
        
        def on_close(self):
            os._exit(os.X_OK)
        
        def __del__(self):
            self.__root.destroy()

    class SS_button:
        def __init__(self, outer) -> None:
            self.__start_button = tk.Button(text="Start", command=lambda: self.toggle_button(self.__start_button))
            self.__working_label = tk.Label(text="Press 1 to start clicking")
            self.__stat_label = tk.Label()
            self.__stop_button = tk.Button(text="Stop",command=lambda: self.toggle_button(self.__stop_button))
            self.y_position = 50
            self.label_y_position = 80
            self.program = outer
            self.__mouse = pp.mouse.Controller()

            self.show_button(self.__start_button)

            self.keyboard_listener()

        #Gui config
        def toggle_button(self, button):
            if(not self.program.working):
                self.program.working = True
                self.stat_label_config("SLEEPING")
                self.hide_button(button)
                self.show_button(self.__stop_button)  
                self.show_label(self.__working_label, self.label_y_position)
                
            else:
                self.program.clicking = False
                self.program.working = False
                self.program.km = False
                self.hide_button(button)
                self.show_button(self.__start_button)       
                self.__working_label.place_forget() 
                self.__stat_label.place_forget()

        def hide_button(self, button):
            button.place_forget()

        def show_button(self, button):
            button.place(y=self.y_position)
            button.update()

            position_x = button.winfo_width()
            position_x = 500/2 - position_x/2

            button.place(x=position_x)

        #show label
        def show_label(self, label, y_position):
            label.place(y=y_position)
            label.update()

            position_x = label.winfo_width()
            position_x = 500/2 - position_x/2

            label.place(x=position_x)

        def stat_label_config(self,word):
            self.__stat_label.config(text=f'current stat : {word}')
            self.show_label(self.__stat_label, 20)

        #keyboard listener
        def keyboard_working(self, key):

            if(key == pp.keyboard.Key.end and self.program.working): 
                self.toggle_button(self.__stop_button)
            elif(key == pp.keyboard.KeyCode(char='1') or key == pp.keyboard.KeyCode(char='1')) and self.program.working:
                self.clicking_start()
            elif((key == pp.keyboard.KeyCode(char='2') or key == pp.keyboard.KeyCode(char='/')) and self.program.working):
                self.program.km = not self.program.km
            elif((key == pp.keyboard.KeyCode(char='c') or key == pp.keyboard.KeyCode(char='แ')) and self.program.km):
                self.__mouse.click(pp.mouse.Button.left, 1)

        def keyboard_listener(self):
            listener = pp.keyboard.Listener(on_press=self.keyboard_working)
            listener.start() #keyboard listener

        #clicking function
        def clicking_working(self):
            delay = self.program.delay_getter()
            while(self.program.clicking):
                self.__mouse.click(pp.mouse.Button.left, 1)
                T.sleep(delay)

        def clicking_start(self):
            if(self.program.clicking):
                self.program.clicking = False
                self.stat_label_config("SLEEPING")
            else:
                self.program.clicking = True
                self.stat_label_config("CLICKING")
                threading_working = TH.Thread(target=self.clicking_working)
                threading_working.start()

def main():
    open = Program()

if __name__ == '__main__':
    main()