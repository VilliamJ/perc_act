# load modules
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
win = visual.Window(fullscr=False, color="black")

# define stop watch
stopwatch = core.Clock()

# get date for a unique logfile name
date = data.getDateStr()

# define logfile
# prepare pandas data frame for recorded data
columns = ['time_stamp', 'id', 'age', 'gender', 'brightness_left', 'size_left', 'hue_left',
           'brightness_right', 'size_right', 'hue_right', 'same_size', 'keypress', 'correct_choice', 'reaction_time']
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
If you understand these rules, please press any key to begin the experiment.
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
    core.wait(0.5)


# show instructions
msg(instruction)


#function for showing circles

def show_circles():
    circle1 = visual.Circle(win, radius = size_left, value_
    

# function for showing circles
def show_circles():
    # Randomize brightness, hue, and size for the left circle
    brightness_left = random.uniform(0.5, 1)
    hue_left = random.uniform(0, 1)
    size_left = random.uniform(0.1, 0.15)
    saturation_left = random.uniform(0.5, 1)

    # Randomize brightness, hue, and size for the right circle
    brightness_right = random.uniform(0.5, 1)
    hue_right = random.uniform(0.5, 1)
    size_right = random.uniform(0.1, 0.15)
    saturation_right = random.uniform(0.5, 1)

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

    return brightness_left, size_left, saturation_left, saturation_right, hue_left, brightness_right, size_right, hue_right, color_rgb_left, color_rgb_right


# preparing circles stimulus
for _ in range(10):
    # show stimulus circles
    brightness_left, size_left, hue_left, saturation_left, brightness_right, size_right, hue_right, saturation_right, color_rgb_left, color_rgb_right = show_circles()

    # start recording reaction time
    stopwatch.reset()

    # check if the circles are the same or different in size
    same_size = 1 if size_left == size_right else 0

    # get response
    response = get_response()

    # check if the participant chose the correct circle (the largest)
    correct_choice = 1 if ((size_left > size_right) and response == 'left') or ((size_left < size_right) and response == 'right') else 0

    # get reaction time
    reaction_time = stopwatch.getTime()

    # record data, appending color information
    logfile = logfile.append({
        'time_stamp': date,
        'id': ID,
        'age': AGE,
        'gender': GENDER,
        'brightness_left': brightness_left,
        'size_left': size_left,
        'hue_left': hue_left,
        'brightness_right': brightness_right,
        'size_right': size_right,
        'hue_right': hue_right,
        'color_left': color_rgb_left,  # Append color information
        'color_right': color_rgb_right,  # Append color information
        'same_size': same_size,
        'keypress': response,
        'correct_choice': correct_choice,
        'reaction_time': reaction_time
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
