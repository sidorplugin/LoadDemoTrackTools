REM Скрипт скачивает с ресурсов "http://www.deejay.de" и "https://juno.co.uk" треки жанра за заданный период

REM Например: get_tracks.bat "D:/Music" house 01.03.2020 01.04.2020 0 5 2000

cd %~dp0

cd ..

echo off

cls

REM d - путь к директории с результатом

REM g - жанр [techno, house, exclusive, ambient], default=techno

REM f - начальная дата поиска, ранняя [dd.mm.yyyy], default=today

REM t - конечная дата поиска, поздняя [dd.mm.yyyy], default=today

REM i - признак загрузки картинок [0,1], default=0

REM s - максимальное время задержки между загрузками в секундах, default=5

REM m - максимальное количество треков в директории, default=2000

echo result path: %~1
echo genre: %~2
echo from date: %~3
echo to date: %~4
echo load image: %~5
echo delay between loads (s): %~6
echo max tracks in dir: %~7

path=%userprofile%/AppData/Local/Programs/Python/Python38-32
python deejayde_tracklist.py house.bin -g %~2 -f %~3 -t %~4 -b 1
python juno_tracklist.py house1.bin -g %~2 -f %~3 -t %~4
python unique_list.py house.bin house1.bin
python track_loader.py output.bin -d %~1 -i %~5 -s %~6 -m %~7

pause