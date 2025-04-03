import tkinter as tk
import time

# Game variables
boat_side = "left"
left_missionaries = 3
left_cannibals = 3
right_missionaries = 0
right_cannibals = 0
on_boat = []

# UI setup
root = tk.Tk()
root.title("Missionaries & Cannibals")
root.geometry("600x400")

canvas = tk.Canvas(root, width=600, height=400, bg="lightblue")
canvas.pack()

# Draw river and land
canvas.create_rectangle(50, 50, 250, 350, fill="green", outline="black")  # Left side
canvas.create_rectangle(350, 50, 550, 350, fill="green", outline="black")  # Right side
canvas.create_rectangle(250, 150, 350, 250, fill="blue", outline="black")  # River

# Boat
boat = canvas.create_rectangle(250, 200, 320, 240, fill="brown")

# Characters
missionaries = [canvas.create_oval(60 + i * 30, 300, 80 + i * 30, 320, fill="white") for i in range(3)]
cannibals = [canvas.create_oval(60 + i * 30, 330, 80 + i * 30, 350, fill="red") for i in range(3)]

# Labels
msg = canvas.create_text(300, 30, text="Move the people safely!", font=("Arial", 12))

def move_boat():
    global boat_side, on_boat, left_missionaries, left_cannibals, right_missionaries, right_cannibals

    if not on_boat:
        canvas.itemconfig(msg, text="Boat must have at least 1 person!")
        return

    # Move boat
    if boat_side == "left":
        for item in on_boat:
            canvas.move(item, 180, 0)
        canvas.move(boat, 180, 0)
        boat_side = "right"
    else:
        for item in on_boat:
            canvas.move(item, -180, 0)
        canvas.move(boat, -180, 0)
        boat_side = "left"

    # Update counts
    left_missionaries = sum(1 for m in missionaries if canvas.coords(m)[0] < 250)
    left_cannibals = sum(1 for c in cannibals if canvas.coords(c)[0] < 250)
    right_missionaries = 3 - left_missionaries
    right_cannibals = 3 - left_cannibals

    # Check win/loss
    if left_missionaries < left_cannibals and left_missionaries > 0:
        canvas.itemconfig(msg, text="Game Over! Cannibals ate the missionaries!")
    elif right_missionaries < right_cannibals and right_missionaries > 0:
        canvas.itemconfig(msg, text="Game Over! Cannibals ate the missionaries!")
    elif right_missionaries == 3 and right_cannibals == 3:
        canvas.itemconfig(msg, text="🎉 You Win! Everyone is safe!")

    # Reset boat
    on_boat.clear()

# Move characters onto the boat
def put_on_boat(event):
    if len(on_boat) < 2:
        item = canvas.find_closest(event.x, event.y)[0]
        if item in missionaries + cannibals:
            if boat_side == "left" and canvas.coords(item)[0] < 250:
                canvas.move(item, 150, -50)
                on_boat.append(item)
            elif boat_side == "right" and canvas.coords(item)[0] > 350:
                canvas.move(item, -150, -50)
                on_boat.append(item)

# Move boat button
move_button = tk.Button(root, text="Move Boat", command=move_boat)
move_button.pack()

canvas.bind("<Button-1>", put_on_boat)

root.mainloop()
