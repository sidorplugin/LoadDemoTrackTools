# coding: utf8
import requests
import random
import funcs
from bs4 import BeautifulSoup
from enum import Enum
from datetime import date, datetime, timezone

source_address = "https://www.juno.co.uk"

# Функция загружает страницу жанра по ссылке.
def load_page(session, page, from_date, to_date, genre):
	url = 'https://www.juno.co.uk/{}/back-cat/{}/?facet[daterange][0]={}TO{}'.format(genre, page, int(from_date), int(to_date))
	request = session.get(url)
	return request.text

# Функция парсит страницу, записывая инфо о треках в таблицу.
def parse_page(text, table, genre, log_file):
	soup = BeautifulSoup(text, 'html.parser')

	i = 0
	albums_size = len(soup('div',{'class':'dv-item'}))

	for albums in soup.findAll('div',{'class':'dv-item'}):
		# Вычисляем процент загрузки.
		percent = round(((i + 1) * 100) / albums_size)
		parse_album(albums, percent, table, genre, log_file)
		i += 1

def get_artist(params):
	return params[0].find('strong').text

def get_album(params):
	return params[1].find('a', {'class': 'text-md'}).text

def get_album_link(params):
	return source_address + params[1].find('a', {'class': 'text-md'}).get('href')

def get_catalog(params):
	div = params[3].text
	catalog = div.split(". Rel: ")[0][5:]
	# Убираем пробелы.
	return catalog.replace(' ', '')
	
def get_label(params):
	label = params[2].text
	return label.lstrip()

def get_date(params):
	div = params[3].text
	return div.split(". Rel: ")[1]

def get_image1(albums):
	try:
		img = albums.find('img',{'class':'lazy_img img-fluid'})
		try:
			if img.get('data-src'):
				image1 = img.get('data-src')
			else:
				image1 = img.get('src')
		except:
			image1 = ""
	except:
		image1 = ""

	if image1 != "":
		image1 = image1.replace('/150/', '/full/').replace('.jpg','-BIG.jpg')
	
	return image1

def get_image2(image1):
	if image1 == "":
		return ""
	return image1.replace('A-BIG.jpg', 'B-BIG.jpg')

# Функция парсит треки в альбоме, записывая результат в таблицу.
def parse_album(albums, percent, table, genre, log_file):
	try:
		params = albums.findAll('div', {'class': 'vi-text'})

		if params == None:
			log_file.write('juno.co.uk: no tag, no data: <div class=vi-text> \n')
			return

		artist = get_artist(params)
		album = get_album(params)
		album_link = get_album_link(params)
		label = get_label(params)
		date = get_date(params)
		catalog = get_catalog(params)
	except:
		log_file.write('juno.co.uk: no tag, no data: <div id=' + albums.get('id') + ' class=vi-text>\n')
		return

	image1 = get_image1(albums)
	if image1 == '':
		log_file.write('juno.co.uk: no image1: <img class=lazy_img img-fluid>; id=' + albums.get('id') + '\n')

	image2 = get_image2(image1)
	if image2 == '':
		log_file.write('juno.co.uk: no image2: <img class=lazy_img img-fluid>; id=' + albums.get('id') + '\n')
	
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
			log_file.write('juno.co.uk: no track: <div class=vi-text>\n')
			continue

# Функция возвращает номер страницы по дате.
def get_max_page(session, genre, from_date, to_date):
	page = 0
	data = load_page(session, 1, from_date.timestamp(), to_date.timestamp(), genre)
	soup = BeautifulSoup(data, 'html.parser')

	try:
		page_data = soup.find('div',{'class':'col-12 col-lg-4 col-xl-auto'}).text
		page = int(page_data.split("1 of ")[1])
	except:
		return page

	return page
