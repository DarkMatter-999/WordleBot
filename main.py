import pyautogui
from PIL import ImageGrab
import pandas as pd
import cv2
import numpy as np

dataset = pd.read_csv("wordle.csv")
start_words = ["React","Adieu","Later","Sired","Tears","Alone","Arise","About","Atone","Irate","Snare","Cream","Paint","Worse","Sauce","Anime","Prowl","Roast","Drape","Media"]

matrix_x_offset = 0.158
matrix_y_offset = 0.069
rows = [(0.13 + matrix_x_offset*i,0.175 + matrix_y_offset*j) for j in range(0,6) for i in range(0,5)]
print(rows)

submit = (0.5, 0.825)

def get_frame(device_name: str):
    window = pyautogui.getWindowsWithTitle(device_name)[0]
    window_x, window_y, window_width, window_height = window.left, window.top, window.width, window.height
    screenshot = ImageGrab.grab(bbox=(window_x, window_y, window_x + window_width, window_y + window_height))
    screenshot.save('game.png')

    return screenshot

frame = np.array(get_frame('moto g51 5G'))
frame = frame[:, :, ::-1].copy()

print(frame.shape)
width, height, _ = frame.shape

for i in rows:
    frame = cv2.circle(frame, (int(i[0]*height), int(i[1]*width)), radius=5, color=(0, 255, 0), thickness=-1)

cv2.imwrite('game.png', frame)


