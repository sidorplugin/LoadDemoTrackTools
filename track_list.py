# Получает треклист по заданным параметрам.
# track_list.py tracks.bin -s deejayde -g house -f xx.xx.2020 -t xx.xx.2020
	# выходной файл для записи
	# s - источник [deejayde, juno, hardwax]
	# g - жанр
	# f - начальная дата поиска, ранняя
	# t - конечная дата поиска, поздняя

import argparse
import requests
import datetime
import sys
import os
import funcs
from bs4 import BeautifulSoup

# Разбор командной строки.
parser = argparse.ArgumentParser()
parser.add_argument ('bin_result', nargs=1)
parser.add_argument ('-s', '--source', choices=['deejayde', 'juno', 'hardwax'], default='deejayde')
parser.add_argument ('-g', '--genre', choices=['techno', 'house', 'exclusive', 'ambient'], default='techno')
parser.add_argument ('-f', '--from_date')
parser.add_argument ('-t', '--to_date')

namespace = parser.parse_args (sys.argv[1:])

tracks_path = namespace.bin_result[0]
source = namespace.source
genre = namespace.genre
from_date = namespace.from_date
to_date = namespace.to_date

# print(tracks_path)
# print(source)
# print(genre)
# print(from_date)
# print(to_date)

# todo Проверки соответствия источника и жанра.
# sys.exit()

s = requests.Session() 
s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
    })

# todo Определяем диапазон страниц которые соответствуют запросу по дате.
# from_page = funcs.get_number_page_by_date(date)
# to_page = funcs.get_number_page_by_date(date)

album_links_path = 'album_links.bin'
from_page = 1
to_page = 1
page = from_page
# Сохраняем ссылки на альбомы в файл album_links.bin.
f = open(album_links_path, 'ab')
# Загружаем контент каждой страницы.
while page <= to_page:
	data = funcs.load_page(page, s)
	# Парсим страницу получая ссылки на альбомы.
	funcs.parse_page(source, f, data)
	print(page, "page parsed")
	page+=1
f.close()

# Открываем файл album_links.bin на чтение.
f = open(album_links_path, 'rb')
# Таблица для сохранения данных.
table = []
# Загружаем контент для каждой ссылки альбома.
for line in f:
	link = line.decode()
	link = link[:-1]
	data = funcs.load_album_page(link, s)
	# Парсим страницу получая информацию о треках.
	funcs.parse_album(source, table, link, data)
f.close()

# Сохраняем информацию о треках в файл tracks.bin.
ft = open(tracks_path, 'wb')
funcs.save_to_file(ft, table)
ft.close()

# Удаляем файл album_links.bin.
os.remove(album_links_path)
