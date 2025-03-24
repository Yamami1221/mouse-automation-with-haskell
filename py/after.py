import pyautogui as pg
import time as t
from pynput import mouse, keyboard
from typing import Callable, List

class Program:

    # constructure
    def __init__(self) -> None:
        # program status
        self.__open: bool = True # program status : close = False, open = True
        self.__running: bool = False # running status : true when running timer and click

        # general instance variable
        # self.__mouse: mouse.Controller = mouse.Controller()
        self.__delay: int = 0
        self.__keyboard_listener = None
        #this for keyboard listener
        # self.list_of_procedure = {
        #     30: self.__toggle_running,
        #     41: self.__close,
        #     33: self.__close_continue
        # }
        self.list_of_procedure = {}
        self.list_of_procedure[49] = self.__toggle_running
        self.list_of_procedure["esc"] = self.__close
        self.list_of_procedure[52] = self.__close_continue

        # [edited1] all type in any too, but have type hint

    def __timer(self, ti: int, sent_output: Callable[[str],None]) -> None: #"higherOrder function"
        """this method for sleep ti second, update every second

        Param: 
            ti: start to count from this to 0
            sent_output: fucntion that will recieve time in string format
                timer may break if have another time in sent_output and continue after sent_output finished
        
        Raises:
            TypeError: when ti is not int
        """

        if(not isinstance(ti, int)): raise TypeError("timer in int only") # [edited2] type validated

        while (ti and self.__running and self.__open):
            mins, secs = divmod(ti, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            sent_output(timer)
            t.sleep(1)
            ti -= 1

    def __ready_to_close(self) -> bool:
        """ this method for check if all thread terminated?
        
        Returns:
            bool: True when ready
        """
        
        check_keyboard_listener : bool = \
            True if (self.__keyboard_listener is None) else (not self.__keyboard_listener.is_alive())
        
        # if(not check_keyboard_listener): print("listener return false now")
        # print(self.__keyboard_listener)
        
        return check_keyboard_listener
    
    
    
    ### program clicking zone
    
    def __recieve_event(self, xs: List[int], ys: List[int], sent_output : Callable[[str],None]) -> None:
        """This method for working to help me play recieve event in some game

        Args:
            xs (List[int]): list of sceen position (X)
            ys (List[int]): list of sceen position (Y)
            sent_output (Callable[[str],None]): procedure for recieve output from timer

        Raises:
            TypeError: when there exit not instance int in xs or ys
        """
        list_size = len(xs)
        
        # validate list type
        for i in range(list_size):
            if(not (isinstance(xs[i], int) and isinstance(ys[i], int))): 
                raise TypeError("list position x or y in not int")
        
        while(self.__open):
            
            if(self.__running):
                for i in range(list_size):
                    if(not self.__running or not self.__open): break
                    
                    t.sleep(1)
                    pg.moveTo(xs[i],ys[i],duration = 0.2)
                    pg.click(xs[i],ys[i])
                self.__timer(self.__delay, sent_output)
                
    def __toggle_running(self): self.__running = not self.__running
    def __close_continue(self): 
        self.__running = False
        return False
    def __close(self, status = False): 
        self.__open = False
        return False
    def __toggle_event(self, key):
        
        if (not open) : return False
        
        do_something = None
        
        if(key == keyboard.Key.esc): do_something = self.list_of_procedure["esc"]
        
        if(hasattr(key, "vk")):
            if(key.vk in self.list_of_procedure):
                do_something = self.list_of_procedure[key.vk]
                
        result = do_something() if (not do_something is None) else None
        # print(result)
                
        if(not (result is None)):
            # print("enter result")
            # print(result)
            return result       
        # print(key.vk)
                
                
    ### choose mode zone
    
    
    
    
    ### public zone ###
    
    def terminate_this(self) -> bool:
        """This method for close program and terminate all thread in this class

        Returns:
            bool: _description_
        """
        self.__open = False
        self.__running = False
        
        while(True):
            if(self.__ready_to_close): 
                print("terminated")
                print("exit ok")
                return True
        
        
        
    ### destructure ###
    
    def __del__(self) -> None:
        self.terminate_this()
        
    
    
    ### test zone
    
    def for_test(self, **kwargs):
    
        sent_output = lambda timer: print(timer, end="\r") # test with lamda expression
        
        if("test_timer" in kwargs) : 
            self.__running = self.__open = True
            self.__timer(kwargs["test_timer"], sent_output=sent_output)
            self.terminate_this()
            
        if(("test_click_x" in kwargs) and ("test_click_y" in kwargs) and ("test_click_timer" in kwargs)):
            self.__running = self.__open = True
            self.__delay = kwargs["test_click_timer"]
            self.__recieve_event(kwargs["test_click_x"], kwargs["test_click_y"], sent_output)
            
    def test_keyboard(self):
        self.__keyboard_listener = keyboard.Listener (on_press=self.__toggle_event)
        self.__keyboard_listener.start()
        
    def getter_ready(self): return self.__ready_to_close()
    
    def __str__(self):
        return "open = "+str(self.__open)+" "+"running = "+str(self.__running)
    
    
    
def main(start: Program):
    # start.for_test(test_timer = 2)1
    
    # X=[269,940,731,1117,956,946,719,1795]
    # Y=[1064,576,819,803,732,943,985,5]

    X=[269,940, 752, 1131, 962, 953 ,719,1795]
    Y=[1064,576, 725, 801, 713, 943 ,985,5]

    start.test_keyboard()
    start.for_test(test_click_x = X, test_click_y = Y, test_click_timer = 900)
    
    while(not start.getter_ready()): 
        print(start)
        pass
        
    
if __name__ == '__main__':
    
    try:
        start = Program()
        main(start)
    except KeyboardInterrupt as e:
        start.terminate_this()
    except Exception as e:
        print(e.__str__())