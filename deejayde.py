# coding: utf8
import requests
import random
import funcs
from bs4 import BeautifulSoup
from enum import Enum
from datetime import date

source_address = "http://www.deejay.de"

# Функция загружает страницу жанра по ссылке.
def load_page(session, page, genre):
	if genre == 'techno':
		url = 'https://www.deejay.de/content.php?param=/m_Techno/sm_News/sort_voe/perpage_160/page_%d' % (page)
	elif genre == 'house':
		url = 'https://www.deejay.de/content.php?param=/m_House/sm_News/sort_voe/perpage_160/page_%d' % (page)
	elif genre == 'exclusive':
		url = 'https://www.deejay.de/content.php?param=/m_Exclusive/sm_News/sort_voe/perpage_160/page_%d' % (page)
	else:
		url = 'https://www.deejay.de/content.php?param=/m_Beats/sm_News/substyles_503_505_519_509/sort_voe/perpage_160/page_%d' % (page)

	request = session.get(url)
	return request.text

# Функция загружает страницу альбома по ссылке.
def load_album_page(session, link):
	url = 'https://www.deejay.de/content.php?param=%s' % (link)
	request = session.get(url)
	return request.text

# Функция парсит альбомы на странице, записывая их в бинарный файл.
def parse_page(source, file, text):	
	soup = BeautifulSoup(text, 'html.parser')

	i = 0
	for albums in soup.findAll('div',{'class':'artikel'}):
		albums_size = len(soup('div',{'class':'artikel'}))
		try:
			album_link = albums.find('h3', {'class': 'title'}).find('a').get('href')
			album_link = source_address + album_link
		except:
			print("warning fetch", album_link)
		
		# Вычисляем процент загрузки. Выводим в консоль.
		percent = round(((i + 1) * 100) / albums_size)
		print('[' + str(percent) + '%]', album_link)

		try:
			album_link += '\n'
			bt = album_link.encode()
			file.write(bt)
		except: 
			print("write error:", album_link)

		i += 1

# Функция формирует ссылку на трек.
# Cсылка формируется следующим образом:
# Из href трека берем только суфикс обозначающий номер трека в альбоме (a, b, c ...). 
# Из href первой картинки берем кусок начинающийся после текста "/xl/",
# к фрагменту "http://www.deejay.de/streamit/" добавляем кусок из href картинки,
# заменяя ".jpg" или ".png" на "суфикс.mp3".
def create_track_link(image_href, track_href):
	link = "http://www.deejay.de/streamit/"
	index = image_href.find("/xl/") + 4
	if index != -1:
		part = image_href[index:]
		link += part
		suffix = track_href[len(track_href) - 1:]
		link = link.replace(".jpg", suffix + ".mp3")
		link = link.replace(".png", suffix + ".mp3")
		return link
	else:
		return ""    

# Функция парсит треки в альбоме, записывая результат в таблицу.
def parse_album(source, table, album_link, text):
	soup = BeautifulSoup(text, 'html.parser')
	try:
		artist = soup.find('div',{'class':'artist'}).find('h1').text
	except:
		artist = ""
		print("warning find artist in:", album_link)
	
	try:    
		album = soup.find('div',{'class':'title'}).find('h1').text
	except:
		album = ""
		print("warning find album in:", album_link)
	
	try:
		genre = soup.find('div',{'class':'styles'}).find('a',{'class':'main'}).find('em').text
	except:
		genre = ""
		print("warning find genre in:", album_link)
	
	try:
		catalog = soup.find('div',{'class':'label'}).find('h1').text
	except:
		catalog = ""
		print("warning find catalog in:", album_link)
	
	try:
		label = soup.find('div',{'class':'label'}).find('h3').text
	except:
		label = ""
		print("warning find label in:", album_link)
	
	try:
		date = soup.find('span',{'class':'date'}).text
		# Убираем в начале строки слово "Release : ".
		date = date[10:]
	except:
		date = ""
		print("warning find date in:", album_link)
	
	try:
		image1 = soup.find('div',{'class':'img allbig img1'}).find('a',{'class':'noMod'}).get('href')
		image1 = source_address + image1
	except:
		try:
			image1 = soup.find('div',{'class':'img img1'}).find('a',{'class':'noMod'}).get('href')
			image1 = source_address + image1
		except:
			image1 = ""
			print("warning find image1 in:", album_link)
	
	try:
		image2 = soup.find('div',{'class':'img allbig img2'}).find('a',{'class':'noMod'}).get('href')
		image2 = source_address + image2
	except:
		try:
			image2 = soup.find('div',{'class':'img img2'}).find('a',{'class':'noMod'}).get('href')
			image2 = source_address + image2
		except:
			image2 = ""
			print("warning find image2 in:", album_link)

	source = "deejay.de"

	soup = BeautifulSoup(text, 'html.parser')
	length = len(table)
	for tracks in soup.findAll('li'):
		try:
			title = tracks.find('a').text
			# Убираем лишние пробелы.
			title = ' '.join(title.split())
			title = title.replace(': ','_')
			
			link = create_track_link (image1, tracks.find('a').get('href'))        
			
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

			print('    ', artist, '-', title)
		except:
			continue

# Функция возвращает номер страницы по дате. Поиск начинается со значения 
# страницы по-умолчанию.
def get_number_page_by_date(session, genre, from_date, bynary_mode, start_page):
	finded = False
	dates_list = []
	searched_date = funcs.get_date_for_string(from_date)
	
	if bynary_mode:
		page = start_page
	else:
		page = 1

	while not finded:
		# Загружаем контент страницы.
		data = load_page(session, page, genre)
		soup = BeautifulSoup(data, 'html.parser')

		# Ищем заголовки дат на странице и заносим их в список.
		for dates in soup.findAll('h2',{'class':'news'}):
			try:
				str_date = dates.find('b').text
				dates_list.append(funcs.get_date_for_string(str_date))
			except:
				print("warning fetch", dates.text)
		
		last = len(dates_list) - 1
		
		if bynary_mode:
			if dates_list[0] <= searched_date < dates_list[last]:
				finded = True
			elif searched_date < dates_list[0]:
				# todo Если проскочили дату задаем новый диапазон и номер страницы.
				page = int(page // 2)
			else:
				# todo Если проскочили дату задаем новый диапазон и номер страницы.
				page = int(page * 2)
		else:
			# Завершаем поиск если искомая дата больше последней даты на странице.
			if searched_date > dates_list[last]:
				finded = True
			else:
				page += 1

		dates_list.clear()
	
	return page
