from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"
timer = None

# ---------------------------- UI SETUP ------------------------------- #
# window
window = Tk()
window.title("Pomodoro")
window.iconbitmap("./download.ico")
window.config(padx=100, pady=75, bg=YELLOW)

# the tomato image and the time
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato = PhotoImage(file="./tomato.png")
canvas.create_image(100, 112, image=tomato)
timer_text = canvas.create_text(100, 130, text="25:00", fill="white", font=(FONT_NAME, 28, "bold"))
canvas.grid(row=1, column=1, padx=25)

# the label in the top center
label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
label.grid(row=0, column=1)

# the ticks to show the number of completions
tick = Label(text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 10, "bold"))
tick.grid(row=3, column=1)
tick.config(pady=10)

# ---------------------------- TIMER MECHANISM ------------------------------- #
no_completed = 0


def start_timer():
    label.config(text="Work", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
    start_button.config(text="Pause", command=pause)
    minutes = WORK_MIN * 60
    count_down(minutes, start_break)


def start_break():
    global no_completed
    no_completed += 1
    if no_completed % 4 == 0:
        label.config(text="Break", fg=RED, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
        seconds = LONG_BREAK_MIN * 60
    else:
        label.config(text="Break", fg=PINK, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
        seconds = SHORT_BREAK_MIN * 60
    count_down(seconds, start_timer)
    increase_check_marks()


def increase_check_marks():
    tick.config(text=CHECK_MARK * no_completed, fg=GREEN, bg=YELLOW, font=(FONT_NAME, 10, "bold"))


def pause():
    start_button.config(text="Resume", command=unpause)


def unpause():
    start_button.config(text="Pause", command=pause)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count, function):
    count_min = count // 60
    count_sec = count % 60
    if count_sec < 10:
        canvas.itemconfig(timer_text, text=f"{count_min}:0{count_sec}")
    elif count_min < 10:
        canvas.itemconfig(timer_text, text=f"0{count_min}:{count_sec}")
    elif count_min < 10 and count_sec < 10:
        canvas.itemconfig(timer_text, text=f"0{count_min}:0{count_sec}")
    else:
        canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count if start_button["text"] == "Resume" else count - 1, function)
    else:
        # Bring the window to the front of the stack
        window.lift()
        window.attributes("-topmost", True)
        window.after_idle(window.attributes, '-topmost', False)
        function()


# ---------------------------- TIMER RESET ------------------------------- #


def reset_button():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="25:00", fill="white", font=(FONT_NAME, 28, "bold"))
    label.config(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
    global no_completed
    no_completed = 0
    tick.config(text=no_completed * CHECK_MARK)
    start_button.config(text="Start", command=start_timer)


start_button = Button(text="Start", command=start_timer)
start_button.grid(row=2, column=0, columnspan=2, sticky="W")

reset_button = Button(text="Reset", command=reset_button)
reset_button.grid(row=2, column=1, columnspan=2, sticky="E")

window.mainloop()
