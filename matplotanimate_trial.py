import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
from threading import Thread
import time
from time import sleep
import random

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

def generate_data():
    while True:
        # create random integer between 0 and 9
        data = random.randint(0, 9)
        time = dt.datetime.now()
        ys.append(data)
        sleep(0.2)

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # Draw x and y lists
    ax.clear()
    ax.plot(xs,ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)


def run_animate():
    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys), interval=1000)
    plt.show()

threading.Thread(target=generate_data).start()
threading.Thread(target=run_animate).start()
