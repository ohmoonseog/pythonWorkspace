# pip install keyboard
import keyboard
import time
import mouse
def fnKeySend():
    time.sleep(0.25) 
    print("====","fnKeySend")
    keyboard.write('userID')
    keyboard.send("tab")
    keyboard.write('Password')
#    keyboard.send("tab,enter")
    fnKeyEnd()

def fnKeyEnd():
    print("end")

def fnKeyStart():
    print("====","fnKeyStart")
    events = []
    mouse.hook(events.append)
    chk = 1
    while chk == 1:
        mouse._listener.queue.join()
        for event in events:
            if isinstance(event, mouse.ButtonEvent):
                if event.button == 'left' and event.event_type == "down":
                    fnKeySend()
                    mouse.unhook_all()
                    chk = 2
                    break
        del events[:]
        time.sleep(0.25)

if __name__ == "__main__":
    keyboard.add_hotkey('ctrl+shift+q', fnKeyStart)
    keyboard.add_abbreviation('@@', 'my.long.email@example.com')
    keyboard.wait('esc')
