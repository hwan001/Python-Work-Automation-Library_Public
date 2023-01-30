import youtube_dl

url="youtube_url"
options = {
    'format':'137' # mp4
}

with youtube_dl.YoutubeDL(options) as ydl:
    ydl.download([url])

print("Done")
