# Загрузчик треков.
# track_loader.py unique_tracks.bin -d "D:/Music" -i 1 -s 1
	# входной файл для записи
	# d - директория для сохранения
	# i - признак загрузки картинок, 0 - не загружать, 1 - загружать.
	# s - признак сортировки по директориям, 0 - все в кучу, 1 - по директориям.s

import requests

tracks_path = 'D:/Work/tracks.bin'

with open(tracks_path, "rb") as ft:
    name = pickle.load(file)
    age = pickle.load(file)
    artist = pickle.load(file)
    title = pickle.load(title)
    album = pickle.load(file)
    genre = pickle.load(file)
    catalog = pickle.load(file)
    label = pickle.load(file)
    date = pickle.load(file)
    link = pickle.load(file)
    album_link = pickle.load(file)
    image1 = pickle.load(file)
    image2 = pickle.load(file)
    source = pickle.load(file)
	print(link)

# mp3 = requests.get(link)

# with open('D:/Work/first.mp3', 'wb') as f:
#     f.write(mp3.content)
# f.close()
ft.close()