from psychopy import visual, event, core

# Create a window
win = visual.Window([800, 600], monitor="testMonitor", units="deg")

# Create text stimuli
description_text = visual.TextStim(win, text="This is a description. Do you agree?", height=1.5)
question_text = visual.TextStim(win, text="Yes (click on 'Agree') or No (click on 'Disagree')?", height=1.5)

# Create mouse
mouse = event.Mouse()

# Set up trial handler
trials = [
    {'description': 'This is a description. Do you agree?', 'correct_response': 'y'},
    # Add more trials as needed
]

for trial in trials:
    # Display description
    description_text.text = trial['description']
    description_text.draw()
    win.flip()

    # Wait for a response
    response = None
    while response is None:
        if mouse.isPressedIn(description_text, buttons=[0]):
            response = 'y'
        elif mouse.isPressedIn(question_text, buttons=[0]):
            response = 'n'

    # Check correctness
    if response == trial['correct_response']:
        feedback_text = visual.TextStim(win, text="Correct!", height=1.5)
    else:
        feedback_text = visual.TextStim(win, text="Incorrect!", height=1.5)

    # Display feedback
    feedback_text.draw()
    win.flip()
    core.wait(1)  # Display feedback for 1 second

# Cleanup
win.close()
core.quit()
