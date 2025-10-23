# Wordle
## Contributed by Võ Đình Cao Minh Hào - 24127035
### Overview
Wordle is a popular guessing word game. This is a self-project contributed by Võ Đình Cao Minh Hào - 24127035, this project is for Computation Thinking Course by VNUHCM-University of Science.

Thank you __**[pythonmcpi](https://github.com/pythonmcpi)**__ for  wordlist dataset: https://github.com/pythonmcpi/wordle-wordlist

### Features

- **Unlimited Plays** - Play as many games as you want
- **Modern UI** - Clean, polished interface with smooth interactions

### How to Play

1. **Guess the word** - Type a 5-letter word using your keyboard and press Enter to submit your guess
3. **Check feedback**:
   - **Green** - Correct letter in correct position
   - **Yellow** - Correct letter in wrong position
   - **Gray** - Letter not in the word
4. **Win** - Guess the word within 6 tries

### Installation

**Python version: 3.11+**

#### 1. Clone the repository 

Clone the repository to your local machine:
```
git clone https://github.com/vdcmhaodl/Wordle
cd Wordle
```
#### 2. Create a Virtual Environment (Optional but Recommended)
Create a virtual environment to avoid conflicts with other projects.
```
python -m venv venv
```

Active it:

- On **Windows**:
    ```
    .\venv\Scripts\activate
    ```
- On **MacOS/Linux**:
    ```
    source venv/bin/activate
    ```
Deactive it:

```
deactivate
```
#### 3. Install Dependencies
Install the required packages using requirements.txt
```
pip install -r requirements.txt
```
#### 4. Run the game
- On **Windows**:
    ```
    py main.py
    ```
- On **MacOS/Linux**:
    ```
    python3 main.py
    ```