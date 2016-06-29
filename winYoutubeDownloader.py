import tkinter as tk
import youtube_dl
import os
from time import strftime

window = tk.Tk()
window.title('Youtube Downloader')
window.geometry('450x200')


class MyLogger(object): #youtube_dl log
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d): #converting message
	if d['status'] == 'finished':
	    print('Done downloading, now converting ...')

def downloader(url): # download file config
	ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	    'logger': MyLogger(),
	    'progress_hooks': [my_hook],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    			ydl.download([url])

def getMusic(url): #main function
	checkYtube = "https://www.youtube.com" # check youtube url
	checkYtubeWatch = "https://www.youtube.com/watch" #check video 
	checkYtubeList = "https://www.youtube.com/playlist" #check playlist
	if (url.startswith(checkYtube)): # check youtube url
		###############Single Video###############
		if(url.startswith(checkYtubeWatch)): #check video 
			if "&" in url: 
				url = url.split("&")[0] 
			print("input a video.")
			print(url)
			if not os.path.exists("singleMusic"):  #confirm the folder isn't exist 
			    os.makedirs("singleMusic") # build a folder to put .mp3 file
			os.chdir("singleMusic") # change dir (cd)
			downloader(url)
			os.chdir("../") # change dir (cd) pwd: {/}
		###############Play List###############
		elif(url.startswith(checkYtubeList)): #check playlist
			print("You input a video list.")
			print("Name your playlist:", end='') # input your playlist name
			now = strftime('%Y-%m-%d %H-%M-%S')
			dir_name = now # folder name

			if not os.path.exists("listMusic"):  #confirm the folder isn't exist
			    os.makedirs("listMusic") # build a folder to put playlist file
			os.chdir("listMusic") # change dir (cd) pwd: listMusic
			if not os.path.exists(dir_name):  #confirm the folder isn't exist
			    os.makedirs(dir_name)

			os.chdir(dir_name) # change dir (cd) pwd: {dir_name}
			downloader(url) #download all the video form the list
			os.chdir("../../") # change dir (cd) pwd: {/}
		else:
			print("Can't download from this URL.")
	else:
		print("Not a youtube URL.")

if __name__ == '__main__':

	l = tk.Label(text='Youtube URL:', font=('Arial', 12), width=15, height=2)
	l.pack()

	e = tk.Entry(window, width=50)
	e.pack()

	def insert_point():
		stat.config(text='Downloading')
		getMusic(e.get())
		stat.config(text='Downloaded Successfully')

	def clear_all():
		stat.config(text=' ')
		e.delete(0,99999999)

	l = tk.Label(text=' ', font=('Arial', 12), width=15, height=1)
	l.pack()

	b1 = tk.Button(window, text='Start Download', width=15,
	              height=2, command=insert_point)
	b1.pack(side="left", expand=True, padx=4, pady=4)
	b2 = tk.Button(window, text='clear', width=15,
	              height=2, command=clear_all)
	b2.pack(side="right", expand=True, padx=4, pady=4)

	stat = tk.Label(text=' ', font=('Arial', 12), width=20, height=1)
	stat.pack()

	window.mainloop()