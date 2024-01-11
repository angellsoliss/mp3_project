import os
from tkinter import *
import pygame
from tkinter import filedialog as fd
import ctypes
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from tkVideoPlayer import TkinterVideo
import random

#create window
window = Tk()
window.title("Music Player")

#define window dimensions
window.geometry("800x415")

#define window color
window.config(bg="linen")

#initialize pygame mixer
pygame.mixer.init()

#loop visualizer
def loopVideo(event):
    videoWindow.play()

#grab random visualizer to load
def randomVisualizer(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        return None
    return os.path.join(folder_path, random.choice(files))

visualisersPath = r"C:\Users\Administrator\codeStuff\projects\python\mp3_project\visualizations"
randomVisualizer = randomVisualizer(visualisersPath)

#create window for visualizer
videoWindow = TkinterVideo(master=window, scaled=True)
videoWindow.load(randomVisualizer)
videoWindow.play()
videoWindow.bind("<<Ended>>", loopVideo)
videoWindow.grid(row=0, column=0, columnspan=5, pady=5, padx=10, sticky="nsew")

#create grid for song controls
controlGrid = Frame(window)
controlGrid.grid(row=5, column=0, sticky="e")
controlGrid.config(bg="linen")

#create playlist songbox
songBox = Listbox(window, font="Fixedsys 5", bg="gray10", fg="linen", width=45, height=20, selectbackground="green2", selectforeground="gray1")
songBox.grid(row=0, column=5, pady=5, padx=20, sticky="nsew")


#create song control icons
prevBtnIcon = PhotoImage(file=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\button_icons\back1.png').subsample(10,10)
nextBtnIcon = PhotoImage(file=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\button_icons\next1.png').subsample(10,10)
pauseBtnIcon = PhotoImage(file=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\button_icons\pause1.png').subsample(10,10)
playBtnIcon = PhotoImage(file=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\button_icons\play1.png').subsample(10,10)
stopBtnIcon = PhotoImage(file=r'C:\Users\Administrator\codeStuff\projects\python\mp3_project\button_icons\stop1.png').subsample(10,10)

#global variable to keep track of whether or not song is paused
global paused
paused = False

#global variable to keep track of if a song has been stopped
global stopped
stopped = False

#define functions for buttons
def prev(): 
    #get index of current song
    currentSongIndex = songBox.curselection()

    #check if any song is selected
    if not currentSongIndex:
        return

    #move to previous song
    prevSongIndex = currentSongIndex[0] - 1

    #chcek if previous song is within the bounds of the list
    if prevSongIndex < songBox.size():
        #get name of song
        songToLoad = songBox.get(prevSongIndex)
        #construct full path to song using song name
        songToLoad = f'C:/Users/Administrator/codeStuff/projects/python/mp3_project/music/{songToLoad}.mp3'
        #load song
        pygame.mixer.music.load(songToLoad)
        #play song once
        pygame.mixer.music.play(loops=0)
        #clear song selection
        songBox.select_clear(0, END)
        #activate previous song
        songBox.activate(prevSongIndex)
        #set selction at previous song
        songBox.selection_set(prevSongIndex, last=None)

def Next():
    #get index of current song
    currentSongIndex = songBox.curselection()
    
    #check if any song is selected
    if not currentSongIndex:
        return
    
    # move to next song
    nextSongIndex = currentSongIndex[0] + 1
    
    #check if next song is within the bounds of the list
    if nextSongIndex < songBox.size():
        #get name of next song
        songToLoad = songBox.get(nextSongIndex)
        #construct full path to song using song name
        songToLoad = f'C:/Users/Administrator/codeStuff/projects/python/mp3_project/music/{songToLoad}.mp3'
        #load song
        pygame.mixer.music.load(songToLoad)
        #play song once
        pygame.mixer.music.play(loops=0)
        #clear song selection
        songBox.select_clear(0, END)
        #activate next song
        songBox.activate(nextSongIndex)
        #set selection at next song
        songBox.selection_set(nextSongIndex, last=None)

#updates play/pause button
def updatePlayPauseIcon():
    if paused:
        playpauseBtn.config(image=pauseBtnIcon)
    else:
        playpauseBtn.config(image=playBtnIcon)

# define functions for buttons
def pause():
    #grab global paused variable
    global paused

    #if song is paused
    if paused:
        #unpause song
        pygame.mixer.music.unpause()
        #update button icon to change to pause
        updatePlayPauseIcon()
        #update global variable
        paused = False
        #unpause visualizer
        videoWindow.play()
    
    #if song is not paused
    else:
        #pause song
        pygame.mixer.music.pause()
        #updaye button icon to change to pause
        updatePlayPauseIcon()
        #update global variable
        paused = True
        #pause visualizer
        videoWindow.pause()

def play():
    #grab global variable stopped
    global stopped
    #update stopped variable to False, indicating a song is playing
    stopped = False
    #get active song name
    songToPlay = songBox.get(ACTIVE)
    #create full path to song using song name 
    songToPlay = f'C:/Users/Administrator/codeStuff/projects/python/mp3_project/music/{songToPlay}.mp3'
    #load and play song
    pygame.mixer.music.load(songToPlay)
    pygame.mixer.music.play()
    #play visualizer video
    videoWindow.play()
    #call songTime to get time elapsed and total length of song
    songTime()

def stop():
    #stop song
    pygame.mixer.music.stop()
    #grab global stopped variable and set to True
    global stopped
    stopped = True
    #pause visualizer
    videoWindow.pause()
    #clear label regarding time
    timeLabel.config(text="")

#commands corresponding to playlist management
def addSong():
    #prompt user to select file from music directory
    songs = fd.askopenfilenames(initialdir=r"C:\Users\Administrator\codeStuff\projects\python\mp3_project\music", title="Choose Files", filetypes=(("mp3 Files", "*.mp3"), ))
    
    #iterate through selected songs
    for song in songs:
        #for each song, remove directory section from song reference, leaving only file name
        song = os.path.basename(song)
        #remove file extension
        song = os.path.splitext(song)[0]
        #insert song to songBox
        songBox.insert(END, song)

def removeOneSong():
    #stop song
    stop()
    #remove highlighted song from songBox
    songBox.delete(ANCHOR)

def removeAllSongs():
    #stop song
    stop()
    #remove all songs from songBox
    songBox.delete(0, END)

#current time/total song length label
timeLabel = Label(window, text="", anchor="w")
timeLabel.grid(row=1, column=0, sticky="nsew")

#volume controls
def volumeSlider(event=None):
    #store current position of slider in variable
    volume = 100 - volSlider.get()
    #set volume level to volume variable
    pygame.mixer.music.set_volume(volume / 100)

def songTime():
    #get time elapsed of current song in secods
    currentTime = pygame.mixer.music.get_pos() / 1000
    
    #convert seconds to minutes
    formattedTime = time.strftime("%M:%S", time.gmtime(currentTime))

    #get current song, add directory information, load song directory with mutagen
    song = songBox.get(ACTIVE)
    song = f'C:/Users/Administrator/codeStuff/projects/python/mp3_project/music/{song}.mp3'
    loadSongWMutagen = MP3(song)

    #make current song length global
    global songLength

    #with the song loaded in mutagen, get song length from file
    songLength = loadSongWMutagen.info.length

    #convert songLength to minutes
    formattedSongLength = time.strftime("%M:%S", time.gmtime(songLength))

    #display time elapsed
    timeLabel.config(text=f"{formattedTime}/{formattedSongLength}")

    #determine if song has ended
    if formattedTime >= formattedSongLength and not stopped:
        #if song has ended, play next song
        Next()

    #update time elapsed recursively
    timeLabel.after(1000, songTime)

#create volume  slider
volSlider = ttk.Scale(window, from_=0, to=100, orient=VERTICAL, command=volumeSlider, length=70, value=0)
volSlider.grid(row=5, column=1, pady=5)

#bind double click action to playing selected song
songBox.bind("<Double-Button-1>", lambda event: play())

#bind space to pause/play
window.bind("<space>", lambda event: pause())

#bind w key to prev
window.bind("<KeyPress-w>", lambda event: prev())

#bind s key to next
window.bind("<KeyPress-s>", lambda event: Next())

#playlist manager bar
mainMenu = Menu(window)
window.config(menu=mainMenu)

#add drop down to add and remove songs to playlist
addRemoveSongsMenu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="Manage Playlist", menu=addRemoveSongsMenu)
addRemoveSongsMenu.add_command(label="Add Songs", command=addSong)
addRemoveSongsMenu.add_command(label="Remove Selected Song", command=removeOneSong)
addRemoveSongsMenu.add_command(label="Remove All Songs", command=removeAllSongs)

#create song control buttons, within button parameters, pack them within controlGrid
prevBtn = Button(controlGrid, image= prevBtnIcon, borderwidth=0, command=prev, bg="linen")
nextBtn = Button(controlGrid, image= nextBtnIcon, borderwidth=0, command=Next, bg="linen")
playpauseBtn = Button(controlGrid, image= pauseBtnIcon, borderwidth=0, command=lambda: pause(), bg="linen")
stopBtn = Button(controlGrid, image= stopBtnIcon, borderwidth=0, command=stop, bg="linen")

#arrange buttons within control grid
stopBtn.grid(row=0, column=0, padx=15)
prevBtn.grid(row=0, column=1, padx=15)
playpauseBtn.grid(row=0, column=2, padx=15)
nextBtn.grid(row=0, column=3, padx=15)

#configure rows and columns so that widgets dynamically resize
for i in range(4):
    window.grid_columnconfigure(i, weight=1)

for i in range(2):
    window.grid_rowconfigure(i, weight=1)
    
window.mainloop()