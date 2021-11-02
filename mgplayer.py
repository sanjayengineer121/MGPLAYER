from tkinter import *
from tkinter import ttk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pygame import mixer
from tkinter import messagebox as mb
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import time


PLAYING = False
stopped = False
silent = False
runningtime = 0
total_time = 0
runningtime_converted = 0
Musics = []
file = ''

''' Create all required function '''

def addmusic():
    fileformat = ['mp3', 'wav', 'mpeg', 'm4a', 'wma', 'ogg']
    global Musics
    directery = filedialog.askdirectory(
        initialdir='Desktop', title='Select Directory')
    os.chdir(directery)
    directeryfiles = os.listdir(directery)
    for file in directeryfiles:
        for ex in fileformat:
            if file.split('.')[-1] == ex:
                playlistbox.insert(END, file.replace('.mp3', ''))
                Musics.append(file)
                status.set('Playlist Updated...')


def fileselect():
    song = filedialog.askopenfilename(
        initialdir='audio/', title="Choose A Song..")
    os.chdir(os.path.dirname(song))
    song = song.split('/')[-1]
    song = song.replace(".mp3", "")
    playlistbox.insert(END, song)
    Musics.append(f'{song}.mp3')


def play():
    global PLAYING
    global stopped

    try:
        if PLAYING == False:
            global file
            file = playlistbox.get(ACTIVE)
            file = f"{file}.mp3"
            mixer.music.load(file)
            mixer.music.play()
            status.set('Playng... - '+str(file.split('.mp3')[0]))
            playbtn['image'] = pause_image
            PLAYING = True
            show_detail(file)

        else:
            if stopped == True:
                mixer.music.unpause()
                status.set('Playng... - '+str(file.split('.mp3')[0]))
                playbtn['image'] = pause_image
                stopped = False
            else:
                mixer.music.pause()
                status.set('Music stopped...')
                playbtn['image'] = play_image
                stopped = True

        Music_play_time()

    except:
        mb.showerror('error', 'No file found to play.')


def Music_play_time():
    runningtime = mixer.music.get_pos()/1000
    runningtime_converted = time.strftime('%M:%S', time.gmtime(runningtime))
    starttime.config(text=runningtime_converted)
    myscroll.config(value=int(runningtime))
    starttime.after(1000, Music_play_time)
    global file
    song = MP3(file)
    global total_time
    total_time = song.info.length
    total_time_converted = time.strftime('%M:%S', time.gmtime(total_time))
    Endtime.config(text=total_time_converted)
    slider_pos = int(total_time)
    myscroll.config(to=slider_pos)


def stop():
    global PLAYING, starttime
    mixer.music.stop()
    PLAYING = False
    playbtn['image'] = play_image
    playlistbox.selection_clear(ACTIVE)
    status.set('Music Stopped...')
    starttime.config(text='00:00')


def previous_song():
    global Musics
    global file
    index = Musics.index(file)-1
    file = Musics[index]
    mixer.music.load(file)
    mixer.music.play()
    status.set('Playng... - '+str(file.split('.mp3')[0]))
    playlistbox.selection_clear(0, END)
    playlistbox.activate(index)
    playlistbox.selection_set(index, last=None)
    show_detail(file)


def upcoming_song():
    global file
    global Musics
    index = Musics.index(file)+1
    file = Musics[index]
    mixer.music.load(file)
    mixer.music.play()
    status.set('Playng... - '+str(file.split('.mp3')[0]))
    playlistbox.selection_clear(0, END)
    playlistbox.activate(index)
    playlistbox.selection_set(index, last=None)
    show_detail(file)


def silent_fun():
    global silent
    if silent == False:
        mixer.music.set_volume(0.0)
        status.set('Music silent..')
        vol_btn['image'] = silent_image
        silent = True
    else:
        mixer.music.set_volume(1.0)
        vol_btn['image'] = vol_image
        status.set('Playng...  -'+str(file.split('.mp3')[0]))
        silent = False

def set_volume(num):
    volume = volume_slider.get()/100
    mixer.music.set_volume(float(volume))

def removesong():
    mixer.music.stop()
    playlistbox.delete(ANCHOR)
    playlistbox.selection_clear(ANCHOR)
    status.set('Song Deleted...')

def delete_allsong():
    mixer.music.stop()
    playlistbox.delete(0, END) 
    status.set('All song deleted...')


def show_detail(play_song):
    with open('temp.jpg', 'wb') as img:
        a = ID3(play_song)
        img.write(a.getall('APIC')[0].data)
        image = makealbumartimage('temp.jpg')
        album_art_label.configure(image=image)
        album_art_label.image = image

def makealbumartimage(image_path):
    image = Image.open(image_path)
    image = image.resize((290, 270), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)

def about():
    mb.showinfo('MGplayer', 'It is the basic music player with some advance feature made in Python.\nIt is created by Er Sanjay Kumar Yadav ❤\nThanks for using the application.👍')

def shortcut_key():
    mb.showinfo('Shortcut Key','1 --  Select a Folder - |ctrl + o|\n2 --  Select a File - |ctrl + l|\n3 --  Delete a song - |Delete|\n4 --  Delete all song - |ctrl + Delete|\n5 --  Exit - |e|\n6 --  Play/Pause - |Spacebar|\n7 --  Select and Play Song - |Double Click Left Mouse Button|\n8 --  Prev Song - |Up Arrow|\n9 --  Next Song - |Down Arrow|\n10 -- Stop - |s|\n11 -- silent - |m| ')

def repeat():
    status.set('Feature Coming Soon.Please Stay with Us.')




''' Main GUI '''
if __name__ == '__main__':
    mixer.init()
    root = Tk()

    root.title("MGplayer")
    root.geometry('800x510')
    root.resizable(height=False, width=False)
    root.iconphoto(True, PhotoImage(file="icon/icon.png"))
    status = StringVar()
    status.set('❤Welcome to MGplayer To U❤')

    mainmenu = Menu(root, tearoff=0)
    filemenu = Menu(mainmenu, tearoff=0)
    filemenu.add_command(label='Folder Select - ctrl + o',font='Helvetica 10 bold', command=addmusic)
    filemenu.add_command(label='File Select - ctrl + l',font='Helvetica 10 bold',  command=fileselect)
    filemenu.add_separator()
    filemenu.add_command(label='Delete a Song - Delete',font='Helvetica 10 bold',  command=removesong)
    filemenu.add_command(label='Delete all song - ctrl + Delete',font='Helvetica 10 bold',  command=delete_allsong)
    filemenu.add_separator()
    filemenu.add_command(label='Exit - e',font='Helvetica 10 bold',  command=exit)
    mainmenu.add_cascade(label='File', menu=filemenu)
    mainmenu.add_command(label='About', command=about)
    mainmenu.add_command(label='Shortcut Key', command=shortcut_key)
    root.config(menu=mainmenu)

    songtrack_frm = LabelFrame(master=root, text="Song Track",font='Helvetica 11 bold',fg='indian red')
    songtrack_frm.place(x=0, y=0, width=350, height=350)

    playlist_frm = LabelFrame(master=root, text="Playlist",font='Helvetica 11 bold',fg='peachpuff4')
    playlist_frm.place(x=350, y=0, width=450, height=350)

    control_frm = LabelFrame(master=root, text="Control Bar",font='Helvetica 11 bold',fg='blue')
    control_frm.place(x=0, y=350, width=800, height=110)

    status_frm = LabelFrame(master=root, text="Song Status",font='Helvetica 11 bold',fg='#6b3a06')
    status_frm.place(x=0, y=460, width=800, height=50)

    s = ttk.Style()
    s.configure('TButton', font='Helvetica 10 bold italic')
    loadbtn = ttk.Button(playlist_frm, text="Load Music", command=addmusic,style='TButton')
    loadbtn.pack()
    x_scroll = ttk.Scrollbar(playlist_frm, orient=HORIZONTAL)
    y_scroll = ttk.Scrollbar(playlist_frm, orient=VERTICAL)
    playlistbox = Listbox(playlist_frm, yscrollcommand=y_scroll.set,
                        xscrollcommand=x_scroll.set, height=350,font='Helvetica 10 italic',fg='#661cac')
    x_scroll.pack(side=BOTTOM, fill=X)
    y_scroll.pack(side=RIGHT, fill=Y)
    x_scroll.config(command=playlistbox.xview)
    y_scroll.config(command=playlistbox.yview)
    playlistbox.pack(fill=BOTH)

    pause_image = PhotoImage(file="icon/pause.png")
    silent_image = PhotoImage(file="icon/mute.png")
    vol_image = PhotoImage(file="icon/vol.png")
    play_image = PhotoImage(file="icon/play.png")
    prev_image = PhotoImage(file="icon/prev.png")
    next_image = PhotoImage(file="icon/next.png")
    stop_image = PhotoImage(file="icon/stop.png")
    repeat_image = PhotoImage(file="icon/repeat.png")
    repeat_one_image = PhotoImage(file="icon/repeat_one.png")
    shuffle_image = PhotoImage(file="icon/shuffle.png")

    album_art_label = Label(songtrack_frm)
    album_art_label.place(x=25, y=25)

    playbtn = Button(control_frm, command=play, image=play_image, bd=0)
    playbtn.place(x=350, y=5)

    def on_enter_play(event):
        play_destination.place(x=325, y=35)

    def on_leave_play(event):
        play_destination.place(x=1000, y=1000)

    playbtn.bind('<Enter>', on_enter_play)
    playbtn.bind('<Leave>', on_leave_play)

    prevbtn = Button(control_frm, image=prev_image, bd=0, command=previous_song)
    prevbtn.place(x=300, y=0)

    def on_enter_prev(event):
        prev_destination.place(x=290, y=35)

    def on_leave_prev(event):
        prev_destination.place(x=1000, y=1000)

    prevbtn.bind('<Enter>', on_enter_prev)
    prevbtn.bind('<Leave>', on_leave_prev)

    nextbtn = Button(control_frm, image=next_image, bd=0, command=upcoming_song)
    nextbtn.place(x=380, y=0)

    def on_enter_next(event):
        next_destination.place(x=365, y=35)

    def on_leave_next(event):
        next_destination.place(x=1000, y=1000)

    nextbtn.bind('<Enter>', on_enter_next)
    nextbtn.bind('<Leave>', on_leave_next)

    stopbtn = Button(control_frm, command=stop, image=stop_image, bd=0)
    stopbtn.place(x=425, y=5)

    def on_enter_stop(event):
        stop_destination.place(x=410, y=35)

    def on_leave_stop(event):
        stop_destination.place(x=1000, y=1000)

    stopbtn.bind('<Enter>', on_enter_stop)
    stopbtn.bind('<Leave>', on_leave_stop)

    vol_btn = Button(control_frm, command=silent_fun, image=vol_image, bd=0)
    vol_btn.place(x=600, y=10)

    def on_enter_vol(event):
        vol_destination.place(x=595, y=35)

    def on_leave_vol(event):
        vol_destination.place(x=1000, y=1000)

    vol_btn.bind('<Enter>', on_enter_vol)
    vol_btn.bind('<Leave>', on_leave_vol)

    repeat_btn = Button(control_frm, image=repeat_image, bd=0, command=repeat)
    repeat_btn.place(x=265, y=7)

    def on_enter_repeat(event):
        repeat_destination.place(x=255, y=35)

    def on_leave_repeat(event):
        repeat_destination.place(x=1000, y=1000)

    repeat_btn.bind('<Enter>', on_enter_repeat)
    repeat_btn.bind('<Leave>', on_leave_repeat)

    global volume_slider
    volume_slider = ttk.Scale(control_frm, from_=0, to=100,
                        orient=HORIZONTAL, command=set_volume                                       ) 
    volume_slider.set(70)
    mixer.music.set_volume(0.7)
    volume_slider.place(x=630, y=8)


    global myscroll
    myscroll = ttk.Scale(control_frm, from_=0, to=100,
                        orient=HORIZONTAL, length=500)
    myscroll.place(x=130, y=50)

    global starttime, Endtime
    starttime = Label(control_frm, text='00:00',font='Helvetica 11 bold',fg='#7f1051')
    starttime.place(x=70, y=50)
    Endtime = Label(control_frm, text='00:00',font='Helvetica 11 bold',fg='#ae6820')
    Endtime.place(x=650, y=50)

    def load_function(event):
        addmusic()

    def file_selection_function(event):
        fileselect()

    def removesong_function(event):
        removesong()

    def delete_all_function(event):
        delete_allsong()

    def Out_function(event):
        stop()
        exit()

    def silent_key_fun(event):
        silent_fun()

    def playing_function(event):
        if event.char == ' ':
            play()

    def play_fun_doublebutton(event):
        stop()
        play()

    def previous_function(event):
        previous_song()

    def upcoming_function(event):
        upcoming_song()

    def Pause_function(event):
        stop()


    root.bind('<Control-o>', load_function)
    root.bind('<Control-l>', file_selection_function)
    root.bind('<Delete>', removesong_function)
    root.bind('<Control-Delete>', delete_all_function)
    root.bind('<e>', Out_function)
    root.bind('<m>', silent_key_fun)
    root.bind('<Key>', playing_function)
    root.bind('<Double-Button-1>', play_fun_doublebutton)
    root.bind('<Up>', previous_function)
    root.bind('<Down>', upcoming_function)
    root.bind('<s>', Pause_function)


    play_destination = Label(control_frm, text='Play/Pause', relief='groove')
    stop_destination = Label(control_frm, text='Stop Music', relief='groove')
    prev_destination = Label(control_frm, text='Previous Track', relief='groove')
    next_destination = Label(control_frm, text='Next Track', relief='groove')
    vol_destination = Label(control_frm, text='silent', relief='groove')
    repeat_destination = Label(control_frm, text='Repeat', relief='groove')


    status_label = Label(status_frm, textvariable=status,font='Helvetica 11 bold',fg='#93c47d')
    status_label.pack()

    root.mainloop()
