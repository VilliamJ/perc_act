from psychopy import visual, core, event, data, gui
import pandas as pd
import os
import random
import colorsys

# define dialogue box (important that this happens before you define the window)
box = gui.Dlg(title="Sizes of Circles")
box.addField("Participant ID: ")
box.addField("Age: ")
box.addField("Gender: ", choices=["Female", "Male", "Other"])

box.show()
if box.OK:  # To retrieve data from the popup window
    ID = box.data[0]
    AGE = box.data[1]
    GENDER = box.data[2]
elif box.Cancel:  # To cancel the experiment if the popup is closed
    core.quit()

# define window
win = visual.Window(fullscr=True, color="black")

# define stop watch
stopwatch = core.Clock()

# get date for a unique logfile name
date = data.getDateStr()

# define logfile
# prepare pandas data frame for recorded data
columns = ['time_stamp', 'id', 'age', 'gender', 'brightness_left', 'size_left', 'hue_left', 'saturation_left',
           'brightness_right', 'size_right', 'hue_right', 'saturation_right', 'color_left', 'color_right',
           'same_size', 'keypress', 'correct_choice', 'reaction_time']
logfile = pd.DataFrame(columns=columns)

# make sure that there is a logfile directory and otherwise make one
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")

# define logfile name
logfile_name = "logfiles/logfile_{}_{}.csv".format(ID, date)

# text
instruction = '''
Welcome to this experiment!\n\n
In a moment, two circles will flash at the same time on the screen. \n\n
Your task is to select the circle you perceive as being the biggest. You do this by pressing either the left or right arrow key on your keyboard. \n\n\n
Before starting please place your hand on the left and right arrow key, so you are ready to answer. If you understand these rules, please press the spacebar to begin and the experiment will begin immediately.
'''

goodbye = '''
The experiment is done. Thank you for your participation
'''



# function for showing text and waiting for a key press
def msg(txt):
    message = visual.TextStim(win, text=txt, alignText="left", height=0.05)
    message.draw()
    win.flip()
    event.waitKeys()
    core.wait(1)

msg(instruction)

def show_circles():
    # Define hue values for red, green, and blue
    red_hue = 1
    green_hue = 1/3
    blue_hue = 2/3
    
    sb_properties = [1, 0.8, 0.6, 0.4]
    
    size_properties =  [0.1, 0.105, 0.11025, 0.11576, 0.12155, 0.12763, 0.13401, 0.14071, 0.14775, 0.15513]

    # Randomly choose one of the three hues
    hue_left = random.choice([red_hue, green_hue, blue_hue])
    hue_right = random.choice([red_hue, green_hue, blue_hue])

    # Randomize other properties
    brightness_left = random.choice(sb_properties)
    size_left = random.choice(size_properties)
    saturation_left = random.choice(sb_properties)

    brightness_right = random.choice(sb_properties)
    size_right = random.choice(size_properties)
    saturation_right = random.choice(sb_properties)

    # Convert RGB to HSV for logging
    color_rgb_left = colorsys.hsv_to_rgb(hue_left, saturation_left, brightness_left)
    color_rgb_right = colorsys.hsv_to_rgb(hue_right, saturation_right, brightness_right)

    circle1 = visual.Circle(win, radius=size_left, fillColor=color_rgb_left, pos=(-0.5, 0))
    circle2 = visual.Circle(win, radius=size_right, fillColor=color_rgb_right, pos=(0.5, 0))
    fixation_cross = visual.TextStim(win, text='+', pos=(0, 0), color='white', height=0.05)

    circle1.draw()
    circle2.draw()
    fixation_cross.draw()
    win.flip()

    core.wait(0.15)

    # clear screen
    win.flip()

    return (
        brightness_left, size_left, hue_left, saturation_left,
        brightness_right, size_right, hue_right, saturation_right,
        color_rgb_left, color_rgb_right
    )

# preparing circles stimulus
for _ in range(50):
    # show stimulus circles
    (
        brightness_left, size_left, hue_left, saturation_left,
        brightness_right, size_right, hue_right, saturation_right,
        color_rgb_left, color_rgb_right
    ) = show_circles()

    # start recording reaction time
    stopwatch.reset()

    # get response
    response = event.waitKeys(keyList=['left', 'right'])[0]

    # check if the participant chose the correct circle (the largest)
    correct_choice = 1 if (
            (size_left > size_right) and response == 'left') or (
            (size_left < size_right) and response == 'right') else 0

    # get reaction time
    reaction_time = stopwatch.getTime()

    # record data, appending color and saturation information
    logfile = logfile.append({
        'time_stamp': date,
        'id': ID,
        'age': AGE,
        'gender': GENDER,
        'brightness_left': round(brightness_left, 2),
        'size_left': round(size_left, 4),
        'hue_left': round(hue_left, 2),
        'saturation_left': round(saturation_left, 2),
        'brightness_right': round(brightness_right, 2),
        'size_right': round(size_right, 4),
        'hue_right': round(hue_right, 2),
        'saturation_right': round(saturation_right, 2),
        'color_left': (round(hue_left, 2), round(saturation_left, 2), round(brightness_left, 2)),
        'color_right': (round(hue_right, 2), round(saturation_right, 2), round(brightness_right, 2)),
        'keypress': response,
        'correct_choice': correct_choice,
        'reaction_time': round(reaction_time, 4)
    }, ignore_index=True)

    # display for 250 ms
    win.flip()
    core.wait(0.15)

    # clear screen
    win.flip()

    # delay before the next trial
    core.wait(0.3)

# save data to directory
logfile.to_csv(logfile_name)

# show goodbye message
msg(goodbye)
