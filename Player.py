import os
import time
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import threading


play_index = 0		# global variables
music_index = 0
t = 0
thread_number = 0
root = Tk()
thread_started = False

menubar = Menu(root)
root.config(menu=menubar)

text = Label(root, text='Lets play the music').pack(side=TOP)

frame = Frame(root)

frame1 = Frame(root)
frame1.pack(side=TOP)

current_length = Label(frame1, text='--:-- /')
current_length.pack(side=LEFT)
total_length_label = Label(frame1, text=' --:--')
total_length_label.pack(side=LEFT)
frame.pack(side=TOP, padx=50, pady=10)
#
filename = ['F:/Charlie_Puth/Charlie Puth -  How Long  [Official Video].mp3',
            'F:/Charlie_Puth/Charlie Puth - BOY [Official Audio].mp3',
            'F:/Charlie_Puth/Charlie Puth - Done For Me (feat. Kehlani) [Official Video].mp3',
            'F:/Charlie_Puth/Charlie Puth - Empty Cups [Official Audio].mp3',
            'F:/Charlie_Puth/Charlie Puth - If You Leave Me Now (feat. Boyz II Men) [Official Audio].mp3',
            'F:/Charlie_Puth/Charlie Puth - LA Girls [Official Audio].mp3',
            'F:/Charlie_Puth/Charlie Puth - Patient [Official Audio].mp3',
            'F:/Charlie_Puth/Charlie Puth - Slow It Down [Official Audio].mp3',
            'F:/Charlie_Puth/Charlie Puth - Somebody Told Me [Official Audio].mp3',
            'F:/Charlie_Puth/Charlie Puth - The Way I Am [Official Lyric Video].mp3',
            'F:/Charlie_Puth/Charlie Puth - Through It All [Official Audio].mp3']

num_music = len(filename) - 1


def browse_file():
    global filename
    global num_music
    global music_index
    filename = list(filedialog.askopenfilenames())
    num_music = len(filename) - 1
    music_index = 0
    play_music()


def about_us():
    tkinter.messagebox.showinfo('About Player', 'This is a music player made by Deepak')


def play_music():
    global t
    global play_index
    global music_index
    global num_music
    if play_index == 0:
        try:
            mixer.music.load(filename[music_index])
            mixer.music.play()
            play_btn['image'] = pausePhoto
            statusbar['text'] = 'Playing Music -  ' + os.path.basename(filename[music_index])
            play_index = -1
            t = 0
            show_details()

        except:
            tkinter.messagebox.showerror('! Error', 'Please select the Music file')

    elif play_index == -1:
        mixer.music.pause()
        play_btn['image'] = playPhoto
        statusbar['text'] = 'Paused Music  -  ' + os.path.basename(filename[music_index])
        play_index = 1

    elif play_index == 1:
        mixer.music.unpause()
        play_btn['image'] = pausePhoto
        statusbar['text'] = 'Playing Music -  ' + os.path.basename(filename[music_index])
        play_index = -1


def stop_music():

    global play_index
    mixer.music.stop()
    statusbar['text'] = 'Music Stopped'
    current_length['text'] = '00:00  / '
    play_btn['image'] = playPhoto
    play_index = 0


def next_music():

    global play_index
    global music_index
    global num_music
    play_index = 0
    if music_index != num_music:
        music_index += 1
        play_music()
    else:
        music_index = 0
        play_music()


def previous_music():

    global play_index
    global music_index
    global num_music
    play_index = 0

    if music_index != 0:
        music_index = music_index - 1
        play_music()
    else:
        music_index = num_music
        play_music()


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)


def show_details():
    global thread_started
    global filename
    global music_index
    file_data = os.path.splitext(filename[music_index])

    if file_data[1] == '.mp3':
        audio = MP3(filename[music_index])
        total_length = audio.info.length
    else:
        a = mixer.Sound(filename[music_index])
        total_length = a.get_length()

    # divmod, split the seconds and minutes
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)

    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    total_length_label['text'] = timeformat
    if not thread_started:
        thread1 = threading.Thread(target=start_count, args=(total_length,))
        thread1.start()
        thread_started = True


def start_count(total_length):
    global t
    global play_index

    while True:
        if t <= total_length and play_index == -1:
            # divmod, split the seconds and minutes
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}  / '.format(mins, secs)
            current_length['text'] = timeformat
            time.sleep(1)
            t += 1.03
            if t >= total_length:
                next_music()
        else:
            continue


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)


mixer.init()    # initializing the mixer

root.minsize(300, 300)
root.maxsize(300, 300)
root.title("Player")

# root.iconbitmap(r'icon.ico') # works in all IDE of windows but not in linux

# works in linux and in windows too
root.call('wm', 'iconphoto', root._w, PhotoImage(file='icon.png'))


playPhoto = PhotoImage(file='play.png')
pausePhoto = PhotoImage(file='pause.png')
play_btn = Button(frame, image=playPhoto, command=play_music)

BackPhoto = PhotoImage(file='back.png')
Back_btn = Button(frame, image=BackPhoto, command=previous_music)
NextPhoto = PhotoImage(file='next.png')
Next_btn = Button(frame, image=NextPhoto, command=next_music)

stopPhoto = PhotoImage(file='stop.png')
stop_btn = Button(root, image=stopPhoto, command=stop_music)


# scale widget
scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(2)
mixer.music.set_volume(.02)   # works also without this statement if volume is note 0


statusbar = Label(root, text="Welcome to my Player", relief=SUNKEN, anchor=W)


Back_btn.pack(side=LEFT, padx=5)
play_btn.pack(side=LEFT, padx=10)
Next_btn.pack(side=LEFT)


statusbar.pack(side=BOTTOM, fill=X)
scale.pack(side=BOTTOM, pady=10)
stop_btn.pack(side=BOTTOM)

root.mainloop()

