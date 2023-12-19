import tkinter
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
rand_word = {}

try:
    df = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    df = pandas.read_csv("./data/german_words.csv")
df_list_of_dicts = df.to_dict(orient="records")


# Generate a random card
def gen_rand_card():
    global rand_word, timer
    window.after_cancel(timer)
    rand_word = random.choice(df_list_of_dicts)
    canvas.itemconfig(card, image=front_img)
    canvas.itemconfig(word, text=rand_word["german"], fill="black")
    canvas.itemconfig(language, text="German", fill="black")

    timer = window.after(3000, flip)


# Flip card
def flip():
    global rand_word
    canvas.itemconfig(card, image=back_img)
    canvas.itemconfig(word, text=rand_word["rus"], fill="white")
    canvas.itemconfig(language, text="Russian", fill="white")


# Delete cleared wort
def del_cleared_w():
    global rand_word
    df_list_of_dicts.remove(rand_word)
    df_to_learn = pandas.DataFrame(df_list_of_dicts, columns=["german", "rus"])
    df_to_learn.to_csv("./data/words_to_learn.csv", index=False)
    gen_rand_card()


# UI
window = tkinter.Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

timer = window.after(3000, flip)

back_img = tkinter.PhotoImage(file="./images/card_back_s.png")
front_img = tkinter.PhotoImage(file="./images/card_front_s.png")
right_img = tkinter.PhotoImage(file="./images/right.png")
wrong_img = tkinter.PhotoImage(file="./images/wrong.png")

canvas = tkinter.Canvas(window, width=500, height=330, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

card = canvas.create_image(250, 165, image=front_img)
word = canvas.create_text(250, 165, text="Word", font=("Ariel", 25, "bold"))
language = canvas.create_text(250, 100, text="Title", font=("Ariel", 15, "italic"))

no_btn = tkinter.Button(image=wrong_img, highlightthickness=0, command=gen_rand_card)
no_btn.grid(column=0, row=1, pady=20)

yes_btn = tkinter.Button(image=right_img, highlightthickness=0, command=del_cleared_w)
yes_btn.grid(column=1, row=1, pady=20)

gen_rand_card()

window.mainloop()
