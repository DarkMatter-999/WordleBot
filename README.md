## Wordle Bot README

This is a Python bot for playing the game Wordle on an Android device. The bot is designed to interact with the game by capturing the game screen, analyzing the colors of the displayed letters, and making intelligent word guesses based on the information gathered.

### Prerequisites
1. Python 3.x
2. Required libraries: pyautogui, PIL (Pillow), pandas, cv2 (OpenCV), numpy

### Setup
1. Clone or download the repository containing your Wordle bot script.
2. Install the required libraries by running: `pip install pyautogui Pillow pandas opencv-python numpy`
3. Create a CSV file named `wordle.csv` with a list of words and their corresponding occurrences. This CSV file will be used as a dataset to make intelligent guesses.

### Running the Bot
1. Connect your Android device to your PC.
2. Use scrcpy or any similar tool to display your Android device's screen on your PC.
3. (Optional) Adjust the `matrix_x_offset` and `matrix_y_offset` values based on the position of the Wordle grid on your Android device's screen.
4. Run the script in your terminal: `python main.py`

### Important Note
Please be aware that automating games using bots can violate the terms of service of the game. Make sure you are not violating any rules or terms before using this bot.

---

## Wordle Bot Documentation
### Overview
The Wordle bot is designed to play the game Wordle on an Android device. It interacts with the game by analyzing the colors of letters on the screen and making guesses to solve the puzzle. The bot uses a dataset of words and their occurrences to make intelligent guesses.

### Functionality
1. **Capturing Frames**

   The bot uses the `get_frame` and `get_opencv_frame` functions to capture frames from the Android device's screen. These frames are then analyzed to determine the colors of letters.

2. **Word Submission**

   The `submit_word` function types a word, moves the cursor to the submit button, and clicks it to submit the guessed word to the game.

3. **Color Analysis**

   The bot analyzes the colors of pixels at specific coordinates to determine the color of a letter. It uses color comparison functions to classify pixels into green (correct letter), yellow (correct letter in the wrong position), and gray (incorrect letter).

4. **Word Guessing Strategy**

   The bot employs a strategy to make intelligent guesses. It filters the dataset based on previously guessed letters' colors and occurrences. It then sorts the dataset by occurrences and selects the most likely word as the next guess.

5. **Main Loop**

   The bot runs a loop to make guesses for each row of letters in the Wordle game. It iterates through the rows, making guesses based on the current information available and updating its guesses as more information is revealed.

### Configuration

- Add your device's name in the `.env` file in the format `device=my-phones-name`
- Adjust the `matrix_x_offset` and `matrix_y_offset` values to match the position of the Wordle grid on your Android device's screen.
- Ensure you have a valid dataset CSV file named `wordle.csv` with word occurrences.

### Running

1. Connect your Android device to your PC and display its screen using a tool like scrcpy.
2. Run the script in your terminal: `python main.py`.
3. The bot will start making guesses based on the analyzed colors and the dataset.

### Important Considerations

- The bot's accuracy and effectiveness depend on the accuracy of color analysis and the quality of the dataset.
- Make sure to comply with the terms of service of the game to avoid any violations or consequences.

