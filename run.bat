cd %~dp0
echo off
cls
python track_list.py tracks.bin -s deejayde -g house -f 10.08.2020 -t 22.09.2020
echo.
python track_loader.py tracks.bin -d d:/Music
pause