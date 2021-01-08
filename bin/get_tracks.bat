REM Скрипт скачивает с ресурсов "http://www.deejay.de" и "https://juno.co.uk" треки жанра за заданный период

REM Например: get_tracks.bat C:/Music house minimal-tech-house 01.03.2020 01.04.2020 0 5 2000

CD %~dp0

CD ..

ECHO off

CLS

ECHO Loading tracks:
ECHO Result path: %~1
ECHO Deejay.de genre: %~2
ECHO Juno genre: %~3
ECHO From date: %~4
ECHO To date: %~5
ECHO Load image: %~6
ECHO Delay between loads (s): %~7
ECHO Max tracks in dir: %~8

REM RESULT_PATH - путь к директории с результатом
REM DJDE_GENRE - жанр [techno, house, exclusive, ambient], default=techno
REM JUNO_GENRE - g - жанр [techno, house, dubstep, electro-house, deep-house, funk-soul-jazz, leftfield, trance-music, downtempo, drumandbass, minimal-tech-house, experimental-electronic], default=techno
REM FROM_DATE - начальная дата поиска, ранняя [dd.mm.yyyy]
REM TO_DATE - конечная дата поиска, поздняя [dd.mm.yyyy]
REM LOAD_IMG - признак загрузки картинок [0,1]
REM DELAY - максимальное время задержки между загрузками в секундах
REM MAX_TRACKS - максимальное количество треков в директории
SET RESULT_PATH=%~1
SET DJDE_GENRE=%~2
SET JUNO_GENRE=%~3
SET FROM_DATE=%~4
SET TO_DATE=%~5
SET LOAD_IMG=%~6
SET DELAY=%~7
SET MAX_TRACKS=%~8

PATH=%userprofile%/AppData/Local/Programs/Python/Python38-32
python deejayde_tracklist.py djde.bin -g %DJDE_GENRE% -f %FROM_DATE% -t %TO_DATE% -b 1
python juno_tracklist.py juno.bin -g %JUNO_GENRE% -f %FROM_DATE% -t %TO_DATE%
python unique_list.py djde.bin juno.bin
python track_loader.py output.bin -d %RESULT_PATH% -i %LOAD_IMG% -s %DELAY% -m %MAX_TRACKS%

pause
