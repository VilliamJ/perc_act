from psychopy import visual, core, event, data, gui
import pandas as pd
import os
import random

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
    core.wait(1)

msg(instruction)

# function for showing circles
def show_circles():
    # Randomize brightness, hue, and size for the left circle
    brightness_left = random.uniform(0.5, 1)
    hue_left = random.uniform(0, 1)
    size_left = random.uniform(0.1, 0.15)
    saturation_left = random.uniform(0.7, 1)

    # Randomize brightness, hue, and size for the right circle
    brightness_right = random.uniform(0.5, 1)
    hue_right = random.uniform(0, 1)
    size_right = random.uniform(0.1, 0.15)
    saturation_right = random.uniform(0.7, 1)

    circle1 = visual.Circle(win, radius=size_left, fillColor=(hue_left, saturation_left, brightness_left), pos=(-0.5, 0))
    circle2 = visual.Circle(win, radius=size_right, fillColor=(hue_right, saturation_right, brightness_right), pos=(0.5, 0))
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
        brightness_right, size_right, hue_right, saturation_right
    )

# preparing circles stimulus
for _ in range(10):
    # show stimulus circles
    (
        brightness_left, size_left, hue_left, saturation_left,
        brightness_right, size_right, hue_right, saturation_right
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
        'size_left': round(size_left, 2),
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
        'reaction_time': round(reaction_time, 2)
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
