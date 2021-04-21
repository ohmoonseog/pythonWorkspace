import mouse
import time

events = []
mouse.hook(events.append)
chk = 1
while chk == 1:
    mouse._listener.queue.join()
    for event in events:
        if isinstance(event, mouse.ButtonEvent):
            if event.button == 'left' and event.event_type == "down":
                print(event)
            elif event.button == 'right' and event.event_type == "down":
                mouse.unhook_all()
                chk = 2
                break
    del events[:]
    time.sleep(0.25)