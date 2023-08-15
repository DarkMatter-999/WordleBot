import pyautogui
from PIL import ImageGrab
import pandas as pd
import cv2
import numpy as np
import random
import time

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
    pyautogui.typewrite(word, interval=0.25)
    pyautogui.moveTo(window.left + submit[0]*window.width, window.top + submit[1]*window.height, 0.25)
    pyautogui.click()
    time.sleep(5)
    
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

def compare_color(realcolor, color, sens):
    color_array = np.array(color)
    
    lower_bound = color_array - sens
    upper_bound = color_array + sens
    
    if np.all((lower_bound <= realcolor) & (realcolor < upper_bound)):
        return True
    else:
        return False

def search_green(df, green):
    string = ["."]*5
    for i in green:
        string[i[1]] = i[0]

    string = "".join(string)
    print(string)
    return df[df["word"].str.contains(string)]

def search_yellow(df, yellow):
    string = ""

    for i in yellow:
        string += "(?=.*" + i +")"

    print(string)
    return df[df["word"].str.contains(f"^{string}.*$")]

def search_gray(df, gray):
    string = "".join(gray)

    print(string)
    return df[df["word"].str.contains(f"^(?!.*[{string}]).*$")]

iter = 0
curr_word = random.choice(start_words).lower()
print(curr_word)
time.sleep(4)
submit_word(curr_word, window)

frame = get_opencv_frame(window)

gray = set()
green = set()
yellow = set()

for i in range(iter,5):
    filter = dataset.copy()
    for j in rows[i]:
        coords = get_coords(width, height, j)
        print(frame[coords[1]][coords[0]])
        if compare_color(frame[coords[1]][coords[0]], (0, 179, 111), 10):
            green.add((curr_word[rows[i].index(j)], rows[i].index(j)))
            if curr_word[rows[i].index(j)] in yellow:
                yellow.discard(curr_word[rows[i].index(j)]) 

        elif compare_color(frame[coords[1]][coords[0]], (0, 164, 215), 10):
            yellow.add(curr_word[rows[i].index(j)])
        
        elif compare_color(frame[coords[1]][coords[0]], (58, 58, 58), 4):
                gray.add(curr_word[rows[i].index(j)])

    gray = gray - {i[0] for i in green}
    gray = gray - yellow
    
    if len(green):
        filter = search_green(filter, green)
    if len(yellow):
        filter = search_yellow(filter, yellow)
    if len(gray):
        filter = search_gray(filter, gray)

    filter.sort_values(by="occurrence", ascending=False, inplace=True)
    filter.reset_index(inplace = True)
    filter.drop("index", inplace = True, axis=1)

    if filter.size <= 0:
        print("Word not found previous was -", curr_word)
        break
    if curr_word == filter["word"].iloc[0]:
        curr_word = filter.sample(n=1)
    else:
        curr_word = filter.iloc[0]["word"]
    print(curr_word)
    print(yellow, green, gray)

    submit_word(curr_word, window)
    frame = get_opencv_frame(window)

print(filter.head(20))
print(yellow, green, gray)



