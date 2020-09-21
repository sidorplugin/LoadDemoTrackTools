# Получает треклист по заданным параметрам.
# track_list.py tracks.bin -s deejayde -g house -f xx.xx.2020 -t xx.xx.2020
	# выходной файл для записи
	# s - источник
	# g - жанр
	# f - начальная дата поиска, ранняя
	# t - конечная дата поиска, поздняя

import requests
import os
import funcs
from bs4 import BeautifulSoup
# establishing session
s = requests.Session() 
s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
    })

# Определяем диапазон страниц которые соответствуют запросу по дате.
# from_page = funcs.get_number_page_by_date(date)
# to_page = funcs.get_number_page_by_date(date)

# todo args
tracks_path = 'tracks.bin'
source = "deejayde"

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
	print(page, "page parsed" + "\n")
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
# Информация о треках в файле:
	# artist,       // Артист.
	# title,        // Название.
	# album,        // Альбом.
	# genre,        // Жанр.
	# catalog,      // Номер по каталогу.
	# label,        // Лэйбл.
	# date,         // Дата выпуска.
	# link,         // Ссылка на трек.
	# album_link,   // Ссылка на альбом.
	# image1,       // Ссылка на 1 изображение.
	# image2,       // Ссылка на 2 изображение.
	# source,       // Ресурс.

