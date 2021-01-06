REM Скрипт скачивает с ресурсов "http://www.deejay.de" и "https://juno.co.uk" треки жанра techno за предыдущий месяц
REM Для автоматизации рекомендуется создать ежемесячную задачу в планировщике;
REM например, 3 числа каждого месяца данная задача будет скачивать techno треки за прошлый месяц.

CD %~dp0

CD ..

ECHO OFF

CLS

SET /A MONTH=%date:~3,2%
SET /A PREVIOUS_MONTH=MONTH-1

SET /A YEAR=%date:~6,4%
SET /A PREVIOUS_YEAR=YEAR-1

REM ROOT_PATH - корневой путь к директории с результатом
SET ROOT_PATH=c:/Music/techno
REM RESULT_PATH - полный путь к директории с результатом
REM FROM_DATE - начальная дата поиска, ранняя [dd.mm.yyyy]
IF "%PREVIOUS_MONTH%"=="0" (SET RESULT_PATH=%ROOT_PATH%/%PREVIOUS_YEAR%/12 & SET FROM_DATE=01.12.%PREVIOUS_YEAR%) ELSE (SET RESULT_PATH=%ROOT_PATH%/%YEAR%/%MONTH% & SET FROM_DATE=01.%PREVIOUS_MONTH%.%YEAR%)

SET MONTH=%date:~3,2%
REM TO_DATE - конечная дата поиска, поздняя [dd.mm.yyyy]
SET TO_DATE=01.%MONTH%.%YEAR%
REM LOAD_IMG - признак загрузки картинок [0,1]
SET LOAD_IMG=0
REM DELAY - максимальное время задержки между загрузками в секундах
SET DELAY=5
REM MAX_TRACKS - максимальное количество треков в директории
SET MAX_TRACKS=2000

ECHO Loading tracks for %FROM_DATE% - %TO_DATE% to %RESULT_PATH%

path=%userprofile%/AppData/Local/Programs/Python/Python38-32
python deejayde_tracklist.py djde.bin -g techno -f %FROM_DATE% -t %TO_DATE% -b 1
python juno_tracklist.py juno.bin -g techno -f %FROM_DATE% -t %TO_DATE%
python unique_list.py djde.bin juno.bin
python track_loader.py output.bin -d %RESULT_PATH% -i %LOAD_IMG% -s %DELAY% -m %MAX_TRACKS%

pause
