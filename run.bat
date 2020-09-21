cd %~dp0
python track_list.py tracks.bin -s deejayde -g house -f 2020.09.10 -t 2020.09.15
python track_loader.py tracks.bin -d d:\Music
pause