cd %~dp0
echo off
cls
echo Parsing tracks...
python track_list.py tracks.bin -s deejayde -g house -f 2020.09.10 -t 2020.09.15
echo.
echo Loading tracks...
python track_loader.py tracks.bin -d d:/Music
echo Done
pause