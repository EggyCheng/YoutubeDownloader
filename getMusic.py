from __future__ import unicode_literals
import youtube_dl
import argparse
import os
from time import strftime
import zipfile

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

def zipdir(path): #zip(compression) the playlist folder
    zipf = zipfile.ZipFile( path+'.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

def getMusic(url): #main function
	checkYtube = "https://www.youtube.com" # check youtube url
	checkYtubeWatch = "https://www.youtube.com/watch" #check video 
	checkYtubeList = "https://www.youtube.com/playlist" #check playlist
	if (url.startswith(checkYtube)): # check youtube url
		###############Single Video###############
		if(url.startswith(checkYtubeWatch)): #check video 
			print("You input a video.")
			os.chdir("singleMusic") # change dir (cd)
			downloader(url)
		###############Play List###############
		elif(url.startswith(checkYtubeList)): #check playlist
			print("You input a video list.")
			print("Name your playlist:", end='') # input your playlist name
			dir_name = input("")
			now = strftime('%Y-%m-%d %H:%M:%S')
			dir_name = dir_name + now # folder name

			os.chdir("listMusic") # change dir (cd) pwd: listMusic
			if not os.path.exists(dir_name):  #confirm the folder isn't exist
			    os.makedirs(dir_name)

			os.chdir(dir_name) # change dir (cd) pwd: {dir_name}
			downloader(url) #download all the video form the list
			#zip the folder to a .zip file
			os.chdir("../") # pwd: listMusic
			zipdir(dir_name) #call compression function
	else:
		print("Not a youtube URL.")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Youtube Downloader.')
	parser.add_argument('-url', type=str, help='the url you want to download.')
	arg = parser.parse_args()
	getMusic(arg.url)