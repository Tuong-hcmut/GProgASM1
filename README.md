# GProgASM1
A game of whack-a-mole featuring zombies.

---

## Setup

### Requirements  
- Python 3.7+  
- pip (Python package manager)  

### Installation  
1. Clone or download this repository.  
2. Open a terminal in the project folder.  
3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
4. Run the game:  
   ```bash
   py main.py
   ```  

---

### Settings  
Game settings can be adjusted directly in **`main.py`**:  

```python
WINDOW_WIDTH  = <desired width>
WINDOW_HEIGHT = <desired height>
FPS           = <desired FPS>
NUM_GRAVES    = <number of graves>
```  

---

## Gameplay  
- Press `Exit` to quit the game, `Settings` to go to settings, and `Play` to play the game.

- In settings and in game, top right of the screen, you can see 2 volume bars, the upper one is for the background music, the lower one is for hit sound.

- The goal of the game is to "hit" the zombies accurately as many times as you can, while minimizing the number of "misses", the relevant stats are displayed at the top right corner of the window.

- In the game, you can see graves at the center of the screens, where zombies spawn from, imminent zombie spawns are indicated by a hand rising from the corresponding grave(s).

- Use your cursor to kill zombies by clicking on them, note that zombies die anyways if you let them live for too long. You will know when you succeed if zombies curl up and blood splatters :D

- Dying zombies, whether by being killed by the player or otherwise, do not count towards "hits" and will count as "misses" when hit, failing to kill zombies will also count as "miss".

- Have fun, and paint the floor red!!! (for approximately 30 frames :< )