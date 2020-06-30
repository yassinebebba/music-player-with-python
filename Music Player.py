from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame

pygame.mixer.init()

song_list = {}
PAUSED = True
CURRENT_SELECTION_INDEX = None


def add_song():
    song = filedialog.askopenfile(initialdir="desktop", filetypes=[("audio files", "*.mp3")])
    *_, song_name = song.name.split("/")
    song_box.insert(END, song_name)
    global song_list
    song_list[song_name] = song.name


def select_song(event=None):
    box = event.widget
    index = int(box.curselection()[0])
    global CURRENT_SELECTION_INDEX, play_pause, play_pause_img, play_pause_icon, PAUSED
    if not CURRENT_SELECTION_INDEX:
        CURRENT_SELECTION_INDEX = index
    elif CURRENT_SELECTION_INDEX != index:
        play_pause_img = Image.open("player icons/play.png")
        play_pause_icon = ImageTk.PhotoImage(play_pause_img)
        play_pause = Button(player_frame, image=play_pause_icon, command=play_pause_song)
        PAUSED = True
        CURRENT_SELECTION_INDEX = index
        play_pause.grid(row=0, column=3, padx=10)
    selected_song = box.get(index)
    selected_song_label['text'] = "You have chosen: " + selected_song


def stop_song():
    pygame.mixer.music.stop()


def refresh_song():
    pygame.mixer.music.play(-1)


def delete_song():
    index = int(song_box.curselection()[0])
    selected_song = song_box.get(index)
    song_box.delete(index)
    global song_list
    del song_list[selected_song]
    song_box.delete(0, END)
    for i in song_list:
        song_box.insert(END, i)


def play_pause_song():
    index = int(song_box.curselection()[0])
    selected_song = song_box.get(index)

    global play_pause, play_pause_img, play_pause_icon, PAUSED
    if PAUSED:
        play_pause_img = Image.open("player icons/pause.png")
        play_pause_icon = ImageTk.PhotoImage(play_pause_img)
        play_pause = Button(player_frame, image=play_pause_icon, command=play_pause_song)
        pygame.mixer.music.load(song_list[selected_song])
        pygame.mixer.music.play(0)
        PAUSED = False
    else:
        play_pause_img = Image.open("player icons/play.png")
        play_pause_icon = ImageTk.PhotoImage(play_pause_img)
        play_pause = Button(player_frame, image=play_pause_icon, command=play_pause_song)
        pygame.mixer.music.pause()
        PAUSED = True
    play_pause.grid(row=0, column=3, padx=10)


def resume_song():
    pygame.mixer.music.unpause()


def rewind_song():
    index = int(song_box.curselection()[0])
    if index - 1 < 0:
        pass
    else:
        selected_song = song_box.curselection()[0]
        song_box.select_clear(index)
        song_box.select_set(index - 1)
        pygame.mixer.music.load(song_list[selected_song])
        selected_song_label['text'] = "You have chosen: " + song_box.grab_current()


root = Tk()
root.title("Music Player")
root.config(bg="#13b096")
root.iconbitmap("player icons/groove.png")
root.geometry("500x400")
song_box = Listbox(root, width=50)
song_box.bind("<<ListboxSelect>>", select_song)
song_box.pack(pady=30)

selected_song_label = Label(root, text="You have not selected a song yet!")
selected_song_label.pack()

player_frame = Frame(root, bd=1, relief=RAISED, bg="#13b096")

add_song_img = Image.open("player icons/add.png")
add_song_icon = ImageTk.PhotoImage(add_song_img)
add_song = Button(player_frame, image=add_song_icon, command=add_song)

rewind_img = Image.open("player icons/rewind.png")
rewind_icon = ImageTk.PhotoImage(rewind_img)
rewind = Button(player_frame, image=rewind_icon, command=rewind_song)

play_pause_img = Image.open("player icons/play.png")
play_pause_icon = ImageTk.PhotoImage(play_pause_img)
play_pause = Button(player_frame, image=play_pause_icon, command=play_pause_song)

forward_img = Image.open("player icons/forward.png")
forward_icon = ImageTk.PhotoImage(forward_img)
forward = Button(player_frame, image=forward_icon)

refresh_img = Image.open("player icons/refresh.png")
refresh_icon = ImageTk.PhotoImage(refresh_img)
refresh = Button(player_frame, image=refresh_icon, command=refresh_song)

delete_img = Image.open("player icons/delete.png")
delete_icon = ImageTk.PhotoImage(delete_img)
delete = Button(player_frame, image=delete_icon, command=delete_song)

favourite_img = Image.open("player icons/favourite.png")
favourite_icon = ImageTk.PhotoImage(favourite_img)
favourite = Button(player_frame, image=favourite_icon, command=resume_song)

add_song.grid(row=0, column=0, padx=10)
favourite.grid(row=0, column=1, padx=10)
rewind.grid(row=0, column=2, padx=10)
play_pause.grid(row=0, column=3, padx=10)
forward.grid(row=0, column=5, padx=10)
refresh.grid(row=0, column=6, padx=10)
delete.grid(row=0, column=7, padx=10)
player_frame.pack(pady=40)
root.mainloop()
