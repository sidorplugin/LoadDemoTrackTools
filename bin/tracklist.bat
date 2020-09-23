cd %~dp0
cd ..
echo off
cls
REM file - выходной файл для записи *.bin
REM s - источник [deejayde, juno, hardwax], default=deejayde
REM g - жанр [techno, house, exclusive, ambient], default=techno
REM f - начальная дата поиска, ранняя [dd.mm.yyyy], default=today
REM t - конечная дата поиска, поздняя [dd.mm.yyyy], default=today
REM b - бинарный поиск даты [0,1], default=0
REM p - стартовая страница поиска максимальной страницы,
REM	    имеет значение только при b = 1, default=150
python track_list.py house2.bin -s deejayde -g house -f 01.02.2020 -t 01.03.2020 -b 1 -p 125
pause