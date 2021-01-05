# Получает суммарный треклист без дубликатов для списка .bin файлов.
# unique_list.py house.bin house1.bin
	# список файлов-треклистов с суфиксом .bin
	# o - путь к файлу с результатом, default='output.bin'

import sys
import argparse

import funcs

# Разбор командной строки.
parser = argparse.ArgumentParser()
parser.add_argument ('bin_files', nargs="*", type=str)
parser.add_argument ('-o', '--output_bin', default='output.bin')

namespace = parser.parse_args (sys.argv[1:])

bin_files = namespace.bin_files
output_bin = namespace.output_bin

# Создаем таблицу для хранения результата.
table = []

# Для каждого bin файла
for bin_file in bin_files:
	print(bin_file, "prepare...")
	# Записываем содержимое файла во временную таблицу
	temp_table = []
	file = open(bin_file, 'rb')
	funcs.table_from_file(temp_table, file)
	file.close()
	
	# Для каждой записи таблицы
	i = 0
	while i < len(temp_table):
		# Считываем track_id записи.
		track_id = temp_table[i][funcs.Track.track_id.value]
		# Если записи с track_id нет в результирующей таблице
		if not funcs.track_exist(table, track_id):
			length = len(table)
			funcs.track_copy(temp_table, i, table, length)
		else:
			artist = temp_table[i][funcs.Track.artist.value]
			title = temp_table[i][funcs.Track.title.value]
			print("Finded dublicate:", "(id: " + track_id + ")", artist, "-", title)
		i += 1
	# Очищаем временную таблицу
	temp_table.clear()

# Сохраняем таблицу в результирующий файл.
ft = open(output_bin, 'wb')
funcs.save_to_file(ft, table)
ft.close()

print("done.")
