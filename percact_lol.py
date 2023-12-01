# load modules
from psychopy import visual, core, event, data, gui
import pandas as pd
import os

# define dialogue box (important that this happens before you define window)
box = gui.Dlg(title="Sizes of Circles")
box.addField("Participant ID: ")
box.addField("Age: ")
box.addField("Gender: ", choices=["Female", "Male", "Other"])

box.show()
if box.OK:  # To retrieve data from popup window
    ID = box.data[0]
    AGE = box.data[1]
    GENDER = box.data[2]
elif box.Cancel:  # To cancel the experiment if popup is closed
    core.quit()

# define window
win = visual.Window(fullscr=False, color="black")

# define stop watch
stopwatch = core.Clock()

# get date for unique logfile name
date = data.getDateStr()

# define logfile
# prepare pandas data frame for recorded data
columns = ['time_stamp', 'id', 'age', 'gender', 'stimulus', 'emotion', 'group', 'age_stimulus', 'keypress',
           'accuracy', 'BAC', 'reaction_time']
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
Your task is to select the circle you perceive as being the biggest. You do this by pressing either the left or right arrow key on your keyboard. If they are the same size, press S on the keyboard.\n\n\n
If you understand these rules, please press any key to begin the experiment.
'''

goodbye = '''
The experiment is done. Thank you for your participation
'''

# function for showing text and waiting for key press
def msg(txt):
    message = visual.TextStim(win, text=txt, alignText="left", height=0.05)
    message.draw()
    win.flip()
    event.waitKeys()


# function for showing circles
def show_circles():
    circle1 = visual.Circle(win, radius=0.05, fillColor='red', pos=(-0.5, 0))
    circle2 = visual.Circle(win, radius=0.06, fillColor='blue', pos=(0.5, 0))
    fixation_cross = visual.TextStim(win, text='+', pos=(0, 0), color='white', height=0.05)

    circle1.draw()
    circle2.draw()
    fixation_cross.draw()
    win.flip()


# function for getting and evaluating a key response
def get_response():
    key = event.waitKeys(keyList=["left", "right", "s"])
    if key[0] == "escape":
        core.quit()
    elif key[0] == "s":
        response = 'same'
    else:
        response = key[0]

    return [response]


# show instructions
msg(instruction)

# preparing circles stimulus
for _ in range(3):  # Repeat the task 3 times (adjust as needed)
    # show stimulus circles
    show_circles()

    # start recording reaction time
    stopwatch.reset()

    # get response
    result = get_response()
    response = result[0]

    # get reaction time
    reaction_time = stopwatch.getTime()

    # record data
    logfile = logfile.append({
        'time_stamp': date,
        'id': ID,
        'age': AGE,
        'gender': GENDER,
        'stimulus': 'NA',  # Circles don't have a specific file path
        'emotion': 'NA',  # Circles don't have emotions, adjust as needed
        'group': 'NA',  # Circles don't belong to a specific group, adjust as needed
        'age_stimulus': 'NA',  # Circles don't have an age, adjust as needed
        'keypress': response,
        'accuracy': 'NA',  # Adjust as needed
        'BAC': 'NA',  # Adjust as needed
        'reaction_time': reaction_time}, ignore_index=True)

# save data to directory
logfile.to_csv(logfile_name)

# show goodbye message
msg(goodbye)
