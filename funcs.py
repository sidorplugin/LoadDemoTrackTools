# coding: utf8
import requests
from bs4 import BeautifulSoup

# todo universal func by genre
def load_page(page, session):
    url = 'https://www.deejay.de/content.php?param=/m_House/sm_News/perpage_160/page_%d' % (page)
    request = session.get(url)
    return request.text

def load_album_page(link, session):
    url = 'https://www.deejay.de/content.php?param=%s' % (link)
    request = session.get(url)
    return request.text

def parse_page(file, text):
    soup = BeautifulSoup(text, 'html.parser')
    for albums in soup.findAll('div',{'class':'artikel'}):
        try:
            # todo разобраться с ошибками выборки
            album_link = albums.find('h3', {'class': 'title'}).find('a').get('href')
        except:
            print("fetch error:", album_link)
        
        try:
            # todo разобраться с кодировкой текста
            album_link += '\n'
            bt = album_link.encode()
            file.write(bt)
        except: 
            print("write error:", album_link)
 
# Cсылка формируется следующим образом:
# из href трека берем только суфикс обозначающий номер трека в альбоме (a, b, c ...). 
# из href первой картинки берем кусок начинающийся после текста "/xl/"
# к фрагменту "http://www.deejay.de/streamit/" добавляем кусок из href картинки,
# заменяя ".jpg" на "суфикс.mp3".
def create_track_link(image_href, track_href):
    link = "http://www.deejay.de/streamit/"
    index = image_href.find("/xl/") + 4
    if index != -1:
        part = image_href[index:]
        link += part
        suffix = track_href[len(track_href) - 1:]
        link = link.replace(".jpg", suffix + ".mp3")
        return link
    else:
        return ""    

def parse_album(table, album_link, text):
    soup = BeautifulSoup(text, 'html.parser')
    try:
        artist = soup.find('div',{'class':'artist'}).find('h1').text
    except:
        artist = ""
        print("fetch error artist in:", album_link)
    
    try:    
        album = soup.find('div',{'class':'title'}).find('h1').text
    except:
        album = ""
        print("fetch error album in:", album_link)
    
    try:
        genre = soup.find('div',{'class':'styles'}).find('a',{'class':'main'}).find('em').text
    except:
        genre = ""
        print("fetch error genre in:", album_link)
    
    try:
        catalog = soup.find('div',{'class':'label'}).find('h1').text
    except:
        catalog = ""
        print("fetch error catalog in:", album_link)
    
    try:
        label = soup.find('div',{'class':'label'}).find('h3').text
    except:
        label = ""
        print("fetch error label in:", album_link)
    
    try:
        date = soup.find('span',{'class':'date'}).text
    except:
        date = ""
        print("fetch error date in:", album_link)
    
    try:
        image1 = soup.find('div',{'class':'img allbig img1'}).find('a',{'class':'noMod'}).get('href')
    except:
        image1 = ""
        print("fetch error image1 in:", album_link)
    
    try:
        image2 = soup.find('div',{'class':'img allbig img2'}).find('a',{'class':'noMod'}).get('href')
    except:
        image2 = ""
        print("fetch error image2 in:", album_link)

    source = "deejay.de"

    soup = BeautifulSoup(text, 'html.parser')
    length = len(table)
    for tracks in soup.findAll('li'):
        try:
            title = tracks.find('a').find('h5').text
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
        except:
            continue    

def save_to_file(file, table):
    # Размер таблицы
    rows = len(table)

    # Конвертируем размеры в строчный тип.
    s_rows = str(rows) + '\n'

    # Конвертируем str в bytes 
    b_rows = s_rows.encode()

    # Записываем размеры в файл.
    file.write(b_rows)

    # Проходим по таблице записывая данные в файл.
    for row in table:
        # Записываем строки с символом '\n'
        for item in row:
            item += '\n'
            bt = item.encode()
            file.write(bt)

# Функция получения таблицы из бинарного файла.
def table_from_file(table, file):
    # Считываем количество строк таблицы из файла.
    s_rows = file.readline()
    rows = int(s_rows)

    # Цикл чтения строк и создание матрицы размером rows*12.
    i = 0
    while i < rows:
        # Создаем одну строку списка.
        row = []
        j = 0
        # Заполняем строки.
        while j < 12:
            bs = file.readline()
            # Конвертируем bytes=>str.
            s = bs.decode()
            # Убираем '\n'.
            s = s[:-1]
            # Добавляем к списку.
            row += [s]
            j += 1

        # Добавляем одну строку списка в таблице.
        table += [row]
        i += 1