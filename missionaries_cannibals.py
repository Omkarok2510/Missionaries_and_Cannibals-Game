import tkinter as tk

# Game variables
boat_side = "left"
left_missionaries = 3
left_cannibals = 3
right_missionaries = 0
right_cannibals = 0
on_boat = []
character_status = {}
move_count = 0

# UI setup
root = tk.Tk()
root.title("Missionaries & Cannibals")
root.geometry("600x450")

canvas = tk.Canvas(root, width=600, height=400, bg="lightblue")
canvas.pack()

# Draw river and land
canvas.create_rectangle(50, 50, 250, 350, fill="green", outline="black")  # Left land
canvas.create_rectangle(350, 50, 550, 350, fill="green", outline="black")  # Right land
canvas.create_rectangle(250, 150, 350, 250, fill="blue", outline="black")  # River

# Boat
boat = canvas.create_rectangle(250, 200, 320, 240, fill="brown")

# Create characters and set initial status
missionaries = []
cannibals = []
for i in range(3):
    m = canvas.create_oval(60 + i * 30, 300, 80 + i * 30, 320, fill="white")
    missionaries.append(m)
    character_status[m] = "left"
    c = canvas.create_oval(60 + i * 30, 330, 80 + i * 30, 350, fill="red")
    cannibals.append(c)
    character_status[c] = "left"

# Labels
msg = canvas.create_text(300, 30, text="Move the people safely!", font=("Arial", 12))
move_label = tk.Label(root, text="Moves: 0", font=("Arial", 10))
move_label.pack()

def update_counts():
    global left_missionaries, left_cannibals, right_missionaries, right_cannibals
    left_missionaries = sum(1 for m in missionaries if character_status[m] == "left")
    left_cannibals = sum(1 for c in cannibals if character_status[c] == "left")
    right_missionaries = 3 - left_missionaries
    right_cannibals = 3 - left_cannibals

def move_boat():
    global boat_side, on_boat, character_status, move_count

    if not on_boat:
        canvas.itemconfig(msg, text="Boat must have at least 1 person!")
        return

    dx = 180 if boat_side == "left" else -180
    for item in on_boat:
        canvas.move(item, dx, 50)  # move to land
        character_status[item] = "right" if boat_side == "left" else "left"
    canvas.move(boat, dx, 0)
    boat_side = "right" if boat_side == "left" else "left"

    update_counts()
    move_count += 1
    move_label.config(text=f"Moves: {move_count}")

    # Win/loss logic
    if left_missionaries < left_cannibals and left_missionaries > 0:
        canvas.itemconfig(msg, text="Game Over! Cannibals ate the missionaries!")
    elif right_missionaries < right_cannibals and right_missionaries > 0:
        canvas.itemconfig(msg, text="Game Over! Cannibals ate the missionaries!")
    elif right_missionaries == 3 and right_cannibals == 3:
        canvas.itemconfig(msg, text="🎉 You Win! Everyone is safe!")

    on_boat.clear()

def put_on_boat(event):
    if len(on_boat) < 2:
        item = canvas.find_closest(event.x, event.y)[0]
        if item in missionaries + cannibals and character_status[item] != "boat":
            if boat_side == "left" and character_status[item] == "left":
                canvas.move(item, 150, -50)
                on_boat.append(item)
                character_status[item] = "boat"
            elif boat_side == "right" and character_status[item] == "right":
                canvas.move(item, -150, -50)
                on_boat.append(item)
                character_status[item] = "boat"

def reset_game():
    global boat_side, move_count, on_boat, character_status

    boat_side = "left"
    on_boat.clear()
    move_count = 0
    move_label.config(text="Moves: 0")
    canvas.itemconfig(msg, text="Move the people safely!")

    canvas.coords(boat, 250, 200, 320, 240)

    # Reset positions and statuses
    for i, m in enumerate(missionaries):
        canvas.coords(m, 60 + i * 30, 300, 80 + i * 30, 320)
        character_status[m] = "left"
    for i, c in enumerate(cannibals):
        canvas.coords(c, 60 + i * 30, 330, 80 + i * 30, 350)
        character_status[c] = "left"

    update_counts()

# Buttons
move_button = tk.Button(root, text="Move Boat", command=move_boat)
move_button.pack()

reset_button = tk.Button(root, text="Reset Game", command=reset_game)
reset_button.pack()

# Event binding
canvas.bind("<Button-1>", put_on_boat)

# Run the app
root.mainloop()
