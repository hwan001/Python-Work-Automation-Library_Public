import youtube_dl

url="https://www.youtube.com/watch?v=jduQ7P6ASgE"
options = {
    'format':'137' # mp4
}

with youtube_dl.YoutubeDL(options) as ydl:
    ydl.download([url])

print("Done")
