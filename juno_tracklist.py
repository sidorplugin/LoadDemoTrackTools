# Получает треклист с ресурса "https://www.juno.co.uk" по заданным параметрам.
# juno_tracklist.py tracks.bin -g house -f dd.mm.yyyy -t dd.mm.yyyy
	# file - выходной файл для записи *.bin
	# g - жанр [techno, house, dubstep, electro, funk-soul-jazz, leftfield, trance-music, downtempo, drumandbass], default=techno
	# f - начальная дата поиска, ранняя [dd.mm.yyyy], default=today
	# t - конечная дата поиска, поздняя [dd.mm.yyyy], default=today

import time
import argparse
import requests
import sys
import os
from datetime import date
from bs4 import BeautifulSoup

import funcs
import juno

# Разбор командной строки.
parser = argparse.ArgumentParser()
parser.add_argument ('bin_result', nargs=1)
parser.add_argument ('-g', '--genre', choices=['techno', 'house', 'leftfield', 'downtempo', 'dubstep', 'electro', 'funk-soul-jazz', 'trance-music', 'drumandbass'], default='techno')
parser.add_argument ('-f', '--from_date', default='')
parser.add_argument ('-t', '--to_date', default='')

namespace = parser.parse_args (sys.argv[1:])

tracks_path = namespace.bin_result[0]
genre = namespace.genre
from_date = namespace.from_date
to_date = namespace.to_date

# Сессия.
s = requests.Session() 
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'})

# Даты по-умолчанию.
if from_date == "":
	from_date = funcs.get_string_for_date(date.today())
	print(from_date)
if to_date == "":
	to_date = funcs.get_string_for_date(date.today())
	print(to_date)

# Определяем количество страниц которые соответствуют запросу.
print('searching pages for date range [' + from_date, '-', to_date + ']')
from_unix_time = funcs.get_date_for_string(from_date)
to_unix_time = funcs.get_date_for_string(to_date)
to_page = juno.get_max_page(s, genre, from_unix_time, to_unix_time)

if to_page == 0:
	print('error: no date for your request.')
	sys.exit()

page = 1

# Таблица для сохранения данных.
table = []

# Загружаем контент с каждой страницы.
print('loading tracks info...')
while page <= to_page:
	print('loading page', page, 'from', to_page)
	data = juno.load_page(s, page, from_unix_time.strftime('%s'), to_unix_time.strftime('%s'), genre)
	# Парсим страницу получая ссылки на треки.
	juno.parse_page(data, table, genre)
	page += 1
print('loading tracks info done.')

# Сохраняем информацию о треках в файл tracks.bin.
ft = open(tracks_path, 'wb')
funcs.save_to_file(ft, table)
ft.close()
