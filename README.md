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

## Credit
- Background music: Plants vs Zombies "LoonBloon"
Original author: Electronic Arts, PopCap Games
Source: https://downloads.khinsider.com/game-soundtracks/album/plants-vs.-zombies

- Hit sfx: Plants vs Zombies "Hammer Strike"
Original author: Electronic Arts, PopCap Games
Source: https://downloads.khinsider.com/game-soundtracks/album/plants-vs.-zombies-2009-gamerip-pc-ios-x360-ps3-ds-android-mobile-psvita-xbox-one-ps4-switch

- Hit vfx: "GIF Free Pixel Effects Pack #5 - Blood Effects"
Original author: XYezawr
Source: https://xyezawr.itch.io/gif-free-pixel-effects-pack-5-blood-effects

- Background assets: "Rogue Fantasy Catacomb" title set.
Original author: Szadi art.
Source: https://szadiart.itch.io/rogue-fantasy-catacombs

- Zombie sprite: "Zombie - simple, becomes projectile"
Original author: IronnButterfly
Source: https://ironnbutterfly.itch.io/zombie-sprite

- Main User Interface assets: "UI User Interface Pack - Horror"
Original author: ToffeeCraft
Source: https://toffeecraft.itch.io/ui-user-interface-pack-horror

- Other User Interface assets: "Pixel Hammer"
Original author: szak
Source: https://en.ac-illust.com/clip-art/26388255/pixel-hammer


