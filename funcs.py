import time
import random
from enum import Enum
from datetime import date

class Track(Enum):
	artist = 0
	title = 1
	album = 2
	genre = 3
	catalog = 4
	publisher = 5
	date = 6
	link = 7
	album_link = 8
	image1 = 9
	image2 = 10
	source = 11

# Функция сохраняет таблицу в файл.
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

def rand_pause(sleep_time):
	rand_time = random.randint(0, sleep_time)
	time.sleep(rand_time)

def get_date_for_string(dd_mm_yyyy):
	return date(int(dd_mm_yyyy[6:]), int(dd_mm_yyyy[4:5]), int(dd_mm_yyyy[:2]))
