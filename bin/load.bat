cd %~dp0

cd ..

echo off

cls

REM входной файл для записи

REM d - директория для сохранения, default=""

REM i - признак загрузки картинок [0,1], default=0

REM s - максимальное время задержки между загрузками, default=5

REM m - максимальное количество треков в директории, default=2000

path=%userprofile%/AppData/Local/Programs/Python/Python38-32
python track_loader.py output.bin -d c:/Music
pause