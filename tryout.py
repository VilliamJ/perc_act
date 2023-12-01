from psychopy import visual, event, core
import random

# Create a window
win = visual.Window([800, 600], color='black')

# Define the control circles
control_circles = [
    {"hue": "red", "saturation": 1.0, "brightness": 1.0},
    {"hue": "blue", "saturation": 1.0, "brightness": 1.0},
    {"hue": "green", "saturation": 1.0, "brightness": 1.0},
]

# Generate variations for saturation
for hue in ["red", "blue", "green"]:
    for saturation in [0.8, 0.6, 0.4, 0.2]:
        control_circles.append({"hue": hue, "saturation": saturation, "brightness": 1.0})

# Generate variations for brightness
for hue in ["red", "blue", "green"]:
    for brightness in [0.8, 0.6, 0.4, 0.2]:
        control_circles.append({"hue": hue, "saturation": 1.0, "brightness": brightness})

# Shuffle the list
random.shuffle(control_circles)

# Create visual stimuli
stimuli = []
for circle_params in control_circles:
    color = (circle_params["brightness"], circle_params["saturation"], 1.0)
    stimuli.append(visual.Circle(win, radius=0.1, fillColorSpace='rgb', fillColor=color))

# Display stimuli
for stimulus in stimuli:
    stimulus.draw()
    win.flip()
    core.wait(1)  # Display each stimulus for 1 second

# Close the window
win.close()
core.quit()
