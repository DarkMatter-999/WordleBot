import pyautogui
from PIL import ImageGrab
import pandas as pd
import cv2
import numpy as np
import random

dataset = pd.read_csv("wordle.csv")
start_words = ["React","Adieu","Later","Sired","Tears","Alone","Arise","About","Atone","Irate","Snare","Cream","Paint","Worse","Sauce","Anime","Prowl","Roast","Drape","Media"]

matrix_x_offset = 0.158
matrix_y_offset = 0.069
rows = [[(0.13 + matrix_x_offset*i,0.175 + matrix_y_offset*j) for i in range(0,5)] for j in range(0,6)]
print(rows)

submit = (0.5, 0.825)

device = ""

with open(".env") as env:
    vars = env.readline()
    vars = vars.split("=")
    if vars[0] == "device":
        device = vars[1].strip()

print(device)

def get_frame(window):
    window_x, window_y, window_width, window_height = window.left, window.top, window.width, window.height
    screenshot = ImageGrab.grab(bbox=(window_x, window_y, window_x + window_width, window_y + window_height))
    return screenshot

def get_opencv_frame(window):
    frame = np.array(get_frame(window))
    frame = frame[:, :, ::-1].copy()
    return frame

def submit_word(word, window):
    pyautogui.typewrite(word, interval=0.1)
    pyautogui.moveTo(window.left + submit[0]*window.width, window.top + submit[1]*window.height, 0.25)
    pyautogui.click()
    
def get_coords(width, height, ratio):
    return (int(ratio[0]*height), int(ratio[1]*width))

window = pyautogui.getWindowsWithTitle(device)[0]

frame = get_opencv_frame(window)

print(frame.shape)
width, height, _ = frame.shape

for j in rows:
    for i in j:
        frame = cv2.circle(frame, get_coords(width, height, i), radius=5, color=(0, 255, 0), thickness=-1)
frame = cv2.circle(frame, get_coords(width, height, submit), radius=10, color=(255,0,0), thickness=-1)

cv2.imwrite('game.png', frame)

iter = 0
curr_word = random.choice(start_words).lower()
curr_word = "snare"
print(curr_word)
#submit_word(curr_word, window)

frame = get_opencv_frame(window)

gray = []
green = []
yellow = []

def compare_color(realcolor, color, sens):
    color_array = np.array(color)
    
    lower_bound = color_array - sens
    upper_bound = color_array + sens
    
    if np.all((lower_bound <= realcolor) & (realcolor < upper_bound)):
        return True
    else:
        return False

for i in range(iter,2):
    for j in rows[i]:
        coords = get_coords(width, height, j)
        print(frame[coords[1]][coords[0]])
        if compare_color(frame[coords[1]][coords[0]], (0, 164, 215), 10):
            yellow.append(curr_word[rows[i].index(j)])

        elif compare_color(frame[coords[1]][coords[0]], (0, 179, 111), 10):
            green.append((curr_word[rows[i].index(j)], rows[i].index[j]))
        
        elif compare_color(frame[coords[1]][coords[0]], (58, 58, 58), 4):
            gray.append(curr_word[rows[i].index(j)])


print(yellow, green, gray)



