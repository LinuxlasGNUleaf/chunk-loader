print('''pregenerator.py - A script to pregenerate chunks in a certain area in minecraft
by teleporting a player in a grid-pattern.

PREREQUISITES:

- linux, because uinput is used
- permissions to use commands in the world (more specifically, the tp command)
- python libraries:
    - evdev
    - pynput
    - tqdm for F R O G
''')
from time import sleep
from pynput.keyboard import Controller
from evdev import uinput, ecodes as e
import sys, math
from tqdm import tqdm

command = "/tp @s {loc_x} {loc_y} {loc_z}\n"
frog = r'''
  __   ___.--'_`.
 ( _`.'. -   'o` )
 _\.'_'      _.-'
( \`. )    //\`
 \_`-'`---'\\__,
  \`        `-\
   `
FROGRESS BAR'''
timestr = lambda sec: f"{int(eta/3600)}h {int((eta%3600)//60)}m {int((eta%3600)%60)}s" 

def mc_command(cmd):
    ui.write(e.EV_KEY, e.KEY_T, 1)
    ui.syn()
    sleep(0.2)
    ui.write(e.EV_KEY, e.KEY_T, 0)
    ui.syn()
    sleep(0.1)
    keyboard.type(cmd)

try:
    print("COLLECTING DATA FOR THE SCAN\n")

    ans = ' '
    while not ans.isdigit():
        ans = input('Input chunk radius of ? (int) ')
        if ans.isdigit():
            ans2 = input(f'This will result in a circle with {int(ans)*32} blocks in diameter. If you are sure, press ENTER, else press ANY OTHER KEY and ENTER. ').strip()
            if ans2 != '':
                ans = ' '
                continue
    rad = abs(int(ans))

    ans = ' '
    while not ans.isdigit() and ans != '':
        ans = input('x/y Resolution of scan? (int, default: 3) ').strip()
    res = abs(int(ans)) if ans else 3

    ans = ' '
    while not ans.isdigit() and ans != '':
        ans = input('Sleep for X seconds at each position (int, default: 10) ')
    sleep_duration = abs(int(ans)) if ans else 10

    int_len = len(str(rad))+1
    total_len = int_len*2 + 4

    tp_pos = []
    for x in range(-rad,rad,res*2):
        for y in range(-rad,rad,res*2):
            if math.sqrt(x**2 + y**2) < rad:
                tp_pos.append((x*16,y*16))

    eta = len(tp_pos)*(sleep_duration+0.5)
    print(f'FINAL CHECK: {len(tp_pos)} positions calculated, each position will load for {sleep_duration} seconds, which (including overhead) approx. totals to: '+timestr(eta))
    input('FINAL CHECK: Confirm the values and press ENTER when you are ready to switch to your Minecraft client.')
except KeyboardInterrupt:
    exit(0)


keyboard = Controller()
ui = uinput.UInput()
print('\n====> START <=====')
print('Alright, let\'s do this!\nKeyboard action will start in 5 seconds. Switch to your MC client, NOW.')
print(frog)
try:
    sleep(5)
    for pos in tqdm (tp_pos, 
                desc="Chunk pregeneration", 
                ascii=False, ncols=100):
        mc_command(command.format(loc_x=pos[0],loc_y='100',loc_z=pos[1]))
        sleep(sleep_duration)
    print("\nChunkloader completed the run successfully.\n=====> END <======")
except KeyboardInterrupt:
    print("\nChunkloader was terminated.\n=====> END <======")
ui.close()