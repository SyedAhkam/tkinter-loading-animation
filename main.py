import time
import threading

from tkinter import Tk, Canvas, Text
from tkinter.font import Font

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

BACKGROUND_COLOR = "white"
CIRCLE_FILL = "lightblue"
CIRCLE_INITIAL_RADIUS = 0
CIRCLE_RADIUS_GROW_PER_FRAME = 5
ANIMATION_FPS = 60
ANIMATION_FRAME_COUNT = 100

def get_circle_coords(x, y, r):
    return (
        x - r, # x1
        y - r, # y1
        x + r, # x2
        y + r  # y2
    )


def create_circle(x, y, r, canvas, **kwargs):
    x1, y1, x2, y2 = get_circle_coords(x, y, r) 

    return canvas.create_oval(x1, y1, x2, y2, **kwargs)

def update_circle(circle_id, canvas, x, y, initial_radius):
    radius = initial_radius

    frame_count = 0
    while frame_count <= ANIMATION_FRAME_COUNT:
        should_sleep = (1 / ANIMATION_FPS) # not sure about the math
        time.sleep(should_sleep)

        x1, y1, x2, y2 = get_circle_coords(x, y, radius)
        canvas.coords(circle_id, x1, y1, x2, y2)
        print(f"Frame: {frame_count} -- Radius: {radius}")

        radius += CIRCLE_RADIUS_GROW_PER_FRAME
        frame_count += 1

    # Clear the circle once animation over
    canvas.delete(circle_id)

def start_update_loop(circle_id, canvas, x, y, r):
    thread = threading.Thread(target=update_circle, args=(circle_id, canvas, x, y, r))
    thread.start()

    return thread

def start_end_poll_loop(draw_thread, execute_after, canvas):
    def poll():
        while True:
            if not draw_thread.is_alive():
                break

        # It died; we may run the callback now
        execute_after(canvas)

    # Start the thread
    threading.Thread(target=poll).start()
    
def start_animation(canvas, execute_after=None):
    x = WINDOW_WIDTH // 2
    y = WINDOW_HEIGHT // 2
    r = CIRCLE_INITIAL_RADIUS

    circle_id = create_circle(
        x,
        y,
        r,
        canvas,
        fill=CIRCLE_FILL,
        outline=BACKGROUND_COLOR
    )

    # Start a background update thread
    update_circle_thread = start_update_loop(circle_id, canvas, x, y, r)
    
    # Spawn another thread which waits until update thread has died (?);
    # Run the `execute_after` function after detected
    if execute_after:
        start_end_poll_loop(update_circle_thread, execute_after, canvas)
        
# Create a Tk instance
root = Tk()

# Set window size
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# Create a canvas
canvas = Canvas(
    root,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    background=BACKGROUND_COLOR
)

# Pack it
canvas.pack()

# Draw widgets to show after animation is done
def draw_ui(canvas):
    canvas.create_text(
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT // 2,
        text="Hello world!",
        font=Font(size=20),
    )

# Show the loading animation
#start_animation(canvas, execute_after=draw_ui) # still working on execute_after; it does work but you know GIL ;-;
start_animation(canvas)

# Enter the main UI loop
root.mainloop()
