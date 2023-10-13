import time
import pyautogui

def detect_hand_position(x, y, scrw, scrh):
    leftarea = (0, 0, scrw // 2, scrh // 2)
    uparea = (0, 0, scrw // 2, scrh // 2)
    downarea = (scrw // 2, scrh // 2, scrw, scrh)
    rightarea = (scrw // 2, scrh // 2, scrw, scrh)

    if x < leftarea[2] and y > leftarea[1]:
        return 'left'
    elif x < uparea[2] and y < uparea[3]:
        return 'up'
    elif x > downarea[0] and y > downarea[1]:
        return 'down'
    elif x > rightarea[0] and y < rightarea[3]:
        return 'right'
    else:
        return None

def stimulate_keys():
    scrw, scrh = pyautogui.size()
    prev_pos = None

    while True:
        x, y = pyautogui.position()
        hand_position = detect_hand_position(x, y, scrw, scrh)
        if hand_position != prev_pos:
            if hand_position == 'left':
                pyautogui.keyDown('left')
                pyautogui.keyUp('right')
                pyautogui.keyUp('up')
                pyautogui.keyUp('down')
            elif hand_position == 'up':
                pyautogui.keyDown('up')
                pyautogui.keyUp('down')
                pyautogui.keyUp('left')
                pyautogui.keyUp('right')
            elif hand_position == 'down':
                pyautogui.keyDown('down')
                pyautogui.keyUp('up')
                pyautogui.keyUp('left')
                pyautogui.keyUp('right')
            elif hand_position == 'right':
                pyautogui.keyDown('right')
                pyautogui.keyUp('left')
                pyautogui.keyUp('up')
                pyautogui.keyUp('down')
            else:
                pyautogui.keyUp('left')
                pyautogui.keyUp('up')
                pyautogui.keyUp('down')
                pyautogui.keyUp('right')
            
            prev_pos = hand_position
        
        time.sleep(0.1) 

if __name__ == "_main_":
    stimulate_keys()
