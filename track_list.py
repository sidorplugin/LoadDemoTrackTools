# Получает треклист по заданным параметрам.
# track_list.py tracks.bin -s deejayde -g house -f dd.mm.yyyy -t dd.mm.yyyy
	# file - выходной файл для записи *.bin
	# s - источник [deejayde, juno, hardwax]
	# g - жанр [techno, house, exclusive, ambient]
	# f - начальная дата поиска, ранняя [dd.mm.yyyy]
	# t - конечная дата поиска, поздняя [dd.mm.yyyy]
	# p - страница с которой начинается бинарный поиск даты (при -b 1)
	# b - бинарный поиск даты [0,1]

import argparse
import requests
import datetime
import sys
import os
from bs4 import BeautifulSoup

import funcs
import deejayde

# Разбор командной строки.
parser = argparse.ArgumentParser()
parser.add_argument ('bin_result', nargs=1)
parser.add_argument ('-s', '--source', choices=['deejayde', 'juno', 'hardwax'], default='deejayde')
parser.add_argument ('-g', '--genre', choices=['techno', 'house', 'exclusive', 'ambient'], default='techno')
parser.add_argument ('-f', '--from_date')
parser.add_argument ('-t', '--to_date')
parser.add_argument ('-p', '--page', default=1)
parser.add_argument ('-b', '--bynary_mode', default=0)

namespace = parser.parse_args (sys.argv[1:])

tracks_path = namespace.bin_result[0]
source = namespace.source
genre = namespace.genre
from_date = namespace.from_date
to_date = namespace.to_date
start_page = namespace.page
bynary_mode = namespace.bynary_mode

# todo Проверки соответствия источника и жанра.

s = requests.Session() 
s.headers.update({
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
		})

# Даты по-умолчанию.
if from_date == "":
	from_date = date.today();
if to_date == "":
	to_date = date.today();

# Определяем диапазон страниц которые соответствуют запросу по дате.
print('searching pages for date range...')
to_page = deejayde.get_number_page_by_date(s, genre, from_date, bynary_mode, start_page)
from_page = deejayde.get_number_page_by_date(s, genre, to_date, bynary_mode, start_page)
print('searching pages for date range done')

albums_path = 'albums.bin'
page = from_page

# Сохраняем ссылки на альбомы в файл albums_path.
f = open(albums_path, 'ab')

# Загружаем контент каждой страницы.
print('loading albums info...')
while page <= to_page:
	print('loading page', page, 'from', to_page)
	data = deejayde.load_page(s, page, genre)
	# Парсим страницу получая ссылки на альбомы.
	deejayde.parse_page(source, f, data)
	page += 1
f.close()
print('loading pages info done.\n')

# Открываем файл albums_path на чтение для определения количества альбомов.
f = open(albums_path, 'rb')
albums_size = sum(1 for line in f)
f.close()

# Таблица для сохранения данных.
table = []

# Открываем файл albums_path на чтение.
f = open(albums_path, 'rb')

# Загружаем контент для каждой ссылки альбома.
print('loading tracks info...')
i = 0
for line in f:
	link = line.decode()
	link = link[:-1]
	data = deejayde.load_album_page(s, link)

	# Вычисляем процент загрузки. Выводим в консоль.
	percent = round(((i + 1) * 100) / albums_size)
	print('[' + str(percent) + '%]', link)
	
	# Парсим страницу получая информацию о треках.
	deejayde.parse_album(source, table, link, data)

	i += 1
f.close()
print('loading tracks info done.')

# Сохраняем информацию о треках в файл tracks.bin.
ft = open(tracks_path, 'wb')
funcs.save_to_file(ft, table)
ft.close()

# Удаляем файл albums_path.
os.remove(albums_path)
