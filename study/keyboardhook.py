# pip install keyboard
import keyboard
import time
def fnKeySend():
    sleepTime = 1
    keyboard.press_and_release('shift+s')
    time.sleep(sleepTime)
    keyboard.press_and_release('space')
    keyboard.write('test2222')
    time.sleep(sleepTime)
    keyboard.press_and_release('\n')
    time.sleep(sleepTime)
    '''    
        time.sleep(sleepTime)
        keyboard.write("GEEKS FOR GEEKS\n") 
        # It writes the keys r, k and endofline  
        keyboard.press_and_release('shift + r, shift + k, \n') 
        keyboard.press_and_release('R, K') 
    '''  
    keyboard.press_and_release('space,tab')
    time.sleep(sleepTime)
    keyboard.write('test333333')    

if __name__ == "__main__":
    keyboard.add_hotkey('ctrl+shift+a', fnKeySend)
#    keyboard.add_hotkey('space', print, args=['space was pressed'])
    keyboard.wait('esc')
'''
GEEKS FOR GEEKS
RK
rk
'''