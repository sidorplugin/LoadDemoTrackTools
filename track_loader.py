# Загрузчик треков.
# track_loader.py tracks.bin -d D:/Music -i 1 -s 5 -m 2000
	# входной файл для записи
	# d - директория для сохранения, default="" 
	# i - признак загрузки картинок [0,1], default=0
	# s - максимальное время задержки между загрузками, default=5
	# m - максимальное количество треков в директории, default=2000

import argparse
import requests
import sys
import os
import funcs
import eyed3

# Разбор командной строки.
parser = argparse.ArgumentParser()
parser.add_argument ('bin_path', nargs=1)
parser.add_argument ('-d', '--dir', default='')
parser.add_argument ('-i', '--img', default=0)
parser.add_argument ('-s', '--sleep', default=5)
parser.add_argument ('-m', '--max', default=2000)

namespace = parser.parse_args (sys.argv[1:])

tracks_path = namespace.bin_path[0]
root_path = namespace.dir
sleep_time = int(namespace.sleep)
max_tracks = int(namespace.max)
load_img = int(namespace.img)

finish_path = ''
cur_album = ''

# Создаем таблицу.
table = []

# Получаем таблицу из бинарного файла.
file = open(tracks_path, 'rb')
funcs.table_from_file(table, file)
file.close()

print('loading files from', tracks_path, 'to', root_path + ':')

# Проход по таблице с сохранением каждого файла.
i = 0
num_path = 1
while i < len(table):
	artist = table[i][funcs.Track.artist.value]
	album = table[i][funcs.Track.album.value]
	title = table[i][funcs.Track.title.value]
	link = table[i][funcs.Track.link.value]
	genre = table[i][funcs.Track.genre.value]
	date = table[i][funcs.Track.date.value]
	publisher = table[i][funcs.Track.publisher.value]
	image1 = table[i][funcs.Track.image1.value]
	image2 = table[i][funcs.Track.image2.value]

	# Создаем директорию для треков.
	if i % max_tracks == 0.0:
		finish_path = root_path + '/' + str(num_path) + '/'
		if not os.path.exists(finish_path):			
			os.makedirs(finish_path)
		num_path += 1

	# Проверяем название артиста и трека на наличие "/", меняем его на "_".
	artist = artist.replace('/', '_').replace('\'', '').replace('|', '').replace('\"', '');
	title = title.replace('/', '_').replace('\'', '').replace('|', '').replace('\"', '');

	# Определяем имя файла.
	file_name = finish_path + artist + ' - ' + title + '.mp3'
	
	# Если файл уже есть обрабатываем следующий.
	if os.path.isfile(file_name):
		i += 1
		continue
	
	# Скачиваем файл по ссылке.
	mp3 = requests.get(link)
	
	# Записываем содержимое в файл.
	with open(file_name, 'wb') as f:
		f.write(mp3.content)
	f.close()

	# Вычисляем процент загрузки. Выводим в консоль.
	percent = round(((i + 1) * 100) / len(table))
	print('[' + str(percent) + '%]', file_name)

	# Записываем ID3 тег в файл.
	audiofile = eyed3.load(file_name)
	if audiofile != None:
		audiofile.tag.artist = artist
		audiofile.tag.title = title
		audiofile.tag.album = album
		audiofile.tag.genre = genre
		# audiofile.tag.release_date = date
		audiofile.tag.publisher = publisher
		audiofile.tag.save()

	# Задерживаем закачку на случайное время.
	funcs.rand_pause(sleep_time)

	# Скачиваем картинки по ссылке.
	if load_img:
		# Создаем директорию для картинок.
		img_path = finish_path + 'img/'
		if not os.path.exists(img_path):
			os.mkdir(img_path)
		
		if not cur_album == album:
			# Скачиваем первый файл по ссылке.
			if not image1 == "":
				img1 = requests.get(image1)
				# Записываем содержимое в файл.
				with open(img_path + album +'1.jpg', 'wb') as f:
					f.write(img1.content)
				f.close()
				print('[' + str(percent) + '%]', image1)

				# Задерживаем закачку на случайное время.
				funcs.rand_pause(sleep_time)

			# Скачиваем второй файл по ссылке.
			if not image2 == "":
				img2 = requests.get(image2)
				# Записываем содержимое в файл.
				with open(img_path + album +'2.jpg', 'wb') as f:
					f.write(img2.content)
				f.close()
				print('[' + str(percent) + '%]', image2)

				# Задерживаем закачку на случайное время.
				funcs.rand_pause(sleep_time)

			cur_album = album

	i += 1

print('loading files done.')
