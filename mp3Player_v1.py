import os
from tkinter import *
import pygame
from tkinter import filedialog
import ctypes
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

myAppId = 'SillyLittleMp3Player'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

window = Tk()
window.title('MP3 Player')
window.geometry('400x355')
window.config(bg='gray1')

#taskbar icon
window.iconbitmap(r"C:\Users\Administrator\codeStuff\projects\python\mp3_project\play-button.png")

#window icon
windowIcon = PhotoImage(file=r"C:\Users\Administrator\codeStuff\projects\python\mp3_project\play-button.png")
window.iconphoto(False, windowIcon)

#initialize pygame mixer
pygame.mixer.init()

#add one song function
def add_song():
    song = filedialog.askopenfilename(initialdir=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\music', title='Choose a song', filetypes=(("mp3 Files", "*.mp3"), ))
    song = os.path.basename(song)
    song = os.path.splitext(song)[0]
    song_list.insert(END, song)

#add multiple songs function
def add_mult_songs():
    songs = filedialog.askopenfilenames(initialdir=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\music', title='Choose a song', filetypes=(("mp3 Files", "*.mp3"), ))

    #loop through song list and replace directory info and file extension
    for song in songs:
        song = os.path.basename(song)
        song = os.path.splitext(song)[0]
        song_list.insert(END, song)

#remove single song from song_list
def delete_song():
    stop()
    song_list.delete(ANCHOR)
    pygame.mixer.music.stop()
    
#remove all songs from song_list
def delete_all():
    stop()
    song_list.delete(0, END)
    pygame.mixer.music.stop()

#play song function
def play():
    global stopped
    stopped = False
    #reset slider position to beginning
    slider.config(value=0)
    #clear time elapsed
    status_bar.config(text='')

    song = song_list.get(ACTIVE)
    song = f'C:/Users/Administrator/codeStuff/projects/python/mp3_project/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #call playtime() function
    playtime()

    #update slider length based on song
    #slider_length = int(song_length)
    #slider.config(to=slider_length, value=0)

global stopped
stopped = False

#stop song function, stops song and will start from beginning when played again
def stop():
    pygame.mixer.music.stop()
    #reset slider position to beginning
    slider.config(value=0)
    song_list.selection_clear(ACTIVE)

    #clear time elapsed
    status_bar.config(text='')

    global stopped
    stopped = True

#next song in song_list
def nxt():
    #reset slider position to beginning
    slider.config(value=0)
    #clear time elapsed
    status_bar.config(text='')

    next_song = song_list.curselection()

    next_song = next_song[0] + 1

    song = song_list.get(next_song)
    song = f'C:/Users/Administrator/codeStuff/projects/python/mp3_project/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_list.selection_clear(0, END)

    song_list.activate(next_song)

    song_list.selection_set(next_song, last=None)

#previous song in song_list
def prev():
    #reset slider position to beginning
    slider.config(value=0)
    #clear time elapsed
    status_bar.config(text='')

    prev_song = song_list.curselection()
    prev_song = prev_song[0] - 1

    song = song_list.get(prev_song)
    song = f'C:/Users/Administrator/codeStuff/projects/python/mp3_project/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_list.selection_clear(0, END)

    song_list.activate(prev_song)

    song_list.selection_set(prev_song, last=None)

#global pause variable, keeps track of whether or not the song is paused,
#so that it can be unpaused or vice versa
global paused
#initially the song is not paused, so paused = False
paused = False

#pause song, next time the song is played, it is played from timestamp when paused
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

#grab playtime elapsed as well as total song length
def playtime():
    #if song is stopped, break out of loop, does not proceed with rest of function
    if stopped:
        return

    #get time elapsed in seconds
    current_time = pygame.mixer.music.get_pos() / 1000

    #temporary diagnostic feature, comparing slider position and actual song position
    #sliderLabel.config(text=f'Slider: {int(slider.get())} and Song Position: {int(current_time)}')
    
    #format time in seconds to minutes:seconds
    converted_time = time.strftime('%M:%S', time.gmtime(current_time))

    #get song that is playing
    song = song_list.get(ACTIVE)
    
    #add directory and mp3 file extension to get length of file
    song = f'C:/Users/Administrator/codeStuff/projects/python/mp3_project/music/{song}.mp3'

    #load song with directory
    load_song_mutagen = MP3(song)

    #make song length global to be referenced in other functions
    global song_length

    #get length from loaded song
    song_length = load_song_mutagen.info.length
    #convert length in seconds to minutes:seconds format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    #eliminate delay between slider and song position
    current_time += 1
    
    #if slider is at the end of the song
    if int(slider.get()) == int(song_length):
        #set the time elapsed to the end of the song
        status_bar.config(text=f'{converted_song_length}/{converted_song_length} ')
        

    #if the position of the slider is at the current position of the song
    #the slider hasn't been moved
    elif int(slider.get()) == int(current_time):
        #update slider length to match length of song
        slider_length = int(song_length)
        slider.config(to=slider_length, value=int(current_time))
    
    #check if song is paused
    elif paused:
        #if song is paused, "pass" over the rest of the checks, stops slider from moving
        pass
    
    #otherwise the slider has been moved
    else:
        #update slider length to match length of song
        slider_length = int(song_length)
        #if the slider has been moved, update the value parameter
        #to the position of the slider
        slider.config(to=slider_length, value=int(slider.get()))

        #convert the time that corresponds to the slider position to minutes:seconds
        converted_time = time.strftime('%M:%S', time.gmtime(int(slider.get())))

        #display current slider time
        status_bar.config(text=f'{converted_time}/{converted_song_length} ')
        
        #have slider keep moving
        keep_sliding = int(slider.get()) + 1
        slider.config(value=keep_sliding)
    
    #update time after every second
    status_bar.after(1000, playtime)

#slide function, corresponds to song position slider
def slide(x):
    #sliderLabel.config(text=f'{int(slider.get())} of {int(song_length)}')
    song = song_list.get(ACTIVE)
    song = f'C:/Users/Administrator/codeStuff/projects/python/mp3_project/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))

#create playlist list box
song_list = Listbox(window, bg="black", fg="green", width=60, selectbackground='MediumPurple3', selectforeground='white' )
song_list.pack(pady=20)

#define control buttons icons
prev_btn_icon = PhotoImage(file=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\button_icons\prev.png').subsample(10,10)
next_btn_icon = PhotoImage(file=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\button_icons\next.png').subsample(10,10)
play_btn_icon = PhotoImage(file=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\button_icons\play.png').subsample(10,10)
pause_btn_icon = PhotoImage(file=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\button_icons\pause.png').subsample(10,10)
stop_btn_icon =  PhotoImage(file=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\button_icons\stop.png').subsample(10,10)

#create frame for buttons
control_frame = Frame(window)
control_frame.pack()
control_frame.config(bg='gray1')

#create control buttons, place buttons on the same row so they are in line with each other
prev_btn = Button(control_frame, image= prev_btn_icon, borderwidth=0, command=prev, bg='gray1')
next_btn = Button(control_frame, image= next_btn_icon, borderwidth=0, command=nxt, bg='gray1')
play_btn = Button(control_frame, image= play_btn_icon, borderwidth=0, command=play, bg='gray1')
pause_btn = Button(control_frame, image= pause_btn_icon, borderwidth=0, command=lambda: pause(paused), bg='gray1')
stop_btn = Button(control_frame, image= stop_btn_icon, borderwidth=0, command=stop, bg='gray1')

prev_btn.grid(row=0, column=0, padx=10)
next_btn.grid(row=0, column=1, padx=10)  
play_btn.grid(row=0, column=2, padx=10)  
pause_btn.grid(row=0, column=3, padx=10)  
stop_btn.grid(row=0, column=4, padx=10)

#create menu to add songs to playlist
my_menu = Menu(window)
window.config(menu=my_menu)

#add label and drop down options to menu tabs
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Add Songs', menu=add_song_menu)
add_song_menu.add_command(label='Add One Song', command=add_song)

#add many songs to playlist
add_song_menu.add_command(label='Add Multiple Songs', command=add_mult_songs)

#create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove Song From Playlist", command= delete_song)
remove_song_menu.add_command(label="Remove All Songs From Playlist", command= delete_all)

#create status bar, holds information about time elapsed
status_bar = Label(window, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#create slider style
sliderStyle = ttk.Style()
#configure style to change color
sliderStyle.configure("TScale", background="gray1")
#define layout for slider
sliderStyle.layout("Tscale.Horizontal.Tscale", [('Horizontal.TScale.slider', {'sticky': 'we'})])

#create song position slider
slider = ttk.Scale(window, from_=0, to=100, orient=HORIZONTAL, command=slide, length=360, value=0, style="TScale")
slider.pack(pady=20)

#temporary slider label
#sliderLabel = Label(window, text="0", bg="gray1", fg="gray")
#sliderLabel.pack(pady=20)

window.mainloop()