# coding: utf8
import requests
import random
import funcs
from bs4 import BeautifulSoup
from enum import Enum
from datetime import date

source_address = "https://www.juno.co.uk"

# Функция загружает страницу жанра по ссылке.
def load_page(session, page, from_date, to_date, genre):
	url = 'https://www.juno.co.uk/{}/back-cat/{}/?facet%5Bdaterange%5D%5B0%5D={}TO{}'.format(genre, page, from_date, to_date)
	request = session.get(url)
	return request.text

# Функция парсит страницу, записывая инфо о треках в таблицу.
def parse_page(text, table, genre):
	soup = BeautifulSoup(text, 'html.parser')

	i = 0
	albums_size = len(soup('div',{'class':'dv-item'}))

	for albums in soup.findAll('div',{'class':'dv-item'}):
		# Вычисляем процент загрузки.
		percent = round(((i + 1) * 100) / albums_size)
		parse_album(albums, percent, table, genre)
		i += 1

# Функция парсит треки в альбоме, записывая результат в таблицу.
def parse_album(albums, percent, table, genre):
	try:
		params = albums.findAll('div', {'class': 'vi-text'})
		artist = params[0].find('strong').text
		album = params[1].find('a', {'class': 'text-md'}).text
		album_link = source_address + params[1].find('a', {'class': 'text-md'}).get('href')
		label = params[2].text
		label = label.lstrip()
		cat_and_date = params[3].text
		date = cat_and_date.split(". Rel: ")[1]
		catalog = cat_and_date.split(". Rel: ")[0][5:]
		# Убираем пробелы.
		catalog = catalog.replace(' ', '')
	except:
		print("error fetch params")

	try:
		img = albums.find('img',{'class':'lazy_img img-fluid'})
		try:
			if img.get('data-src'):
				image1 = img.get('data-src')
			else:
				image1 = img.get('src')
		except:
			print("warning find image")
	except:
		print("warning find image")

	image1 = image1.replace('/150/', '/300/').replace('.jpg','-MED.jpg')
	image2 = image1.replace('A-MED.jpg', 'B-MED.jpg')
	source = "juno.co.uk"

	length = len(table)
	num = 1
	for tracks in albums.findAll('li'):
		try:
			title = tracks.find('div', {'class': 'vi-text'}).text
			# Убираем лишние пробелы.
			title = ' '.join(title.split())
			track_id = "%s_%d" % (catalog, num)
			link = tracks.find('a', {'class': 'jrplayer'}).get('href')
			
			# Заполняем таблицу данными.
			table.append([])
			table[length].append(artist)
			table[length].append(title)
			table[length].append(album)
			table[length].append(genre)
			table[length].append(catalog)
			table[length].append(label)
			table[length].append(date)
			table[length].append(link)
			table[length].append(album_link)
			table[length].append(image1)
			table[length].append(image2)
			table[length].append(source)
			table[length].append(track_id)
			
			print('[' + str(percent) + '%]:', artist, '-', title)

			num += 1
		except:
			continue

# Функция возвращает номер страницы по дате.
def get_max_page(session, genre, from_date, to_date):
	page = 0
	data = load_page(session, 1, from_date.strftime('%s'), to_date.strftime('%s'), genre)
	soup = BeautifulSoup(data, 'html.parser')

	try:
		page_data = soup.find('div',{'class':'col-12 col-lg-4 col-xl-auto'}).text
		page = int(page_data.split("1 of ")[1])
	except:
		print("no pages:")
		return page

	return page
