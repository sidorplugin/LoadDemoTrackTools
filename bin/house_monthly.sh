#!/bin/bash

# Скрипт скачивает с ресурсов "http://www.deejay.de" и "https://juno.co.uk" треки жанра house за предыдущий месяц
# Для автоматизации рекомендуется создать ежемесячную задачу в планировщике;
# например, 3 числа каждого месяца данная задача будет скачивать house треки за прошлый месяц.

MONTH=`date +%m`
LAST_MONTH=`date +%m --date="last month"`

YEAR=`date +%Y`
LAST_YEAR=`date +%Y --date="last year"`

# ROOT_PATH - корневой путь к директории с результатом
ROOT_PATH="/home/sidormax/music/house"
# RESULT_PATH - полный путь к директории с результатом
# FROM_DATE - начальная дата поиска, ранняя [dd.mm.yyyy]
if [ $MONTH -eq "01" ]
then
  RESULT_PATH=$ROOT_PATH"/"$LAST_YEAR"/"$LAST_MONTH
  FROM_DATE="01."$LAST_MONTH"."$LAST_YEAR
else
  RESULT_PATH=$ROOT_PATH"/"$YEAR"/"$MONTH
  FROM_DATE="01."$LAST_MONTH"."$YEAR
fi

# TO_DATE - конечная дата поиска, поздняя [dd.mm.yyyy]
TO_DATE="01."$MONTH"."$YEAR
# LOAD_IMG - признак загрузки картинок [0,1]
LOAD_IMG="0"
# DELAY - максимальное время задержки между загрузками в секундах
DELAY="0"
# MAX_TRACKS - максимальное количество треков в директории
MAX_TRACKS="2000"

echo "Loading tracks for" $FROM_DATE "-" $TO_DATE "to" $RESULT_PATH

cd ..
python3 deejayde_tracklist.py djde.bin -g house -f $FROM_DATE -t $TO_DATE -b 1
python3 juno_tracklist.py juno.bin -g house -f $FROM_DATE -t $TO_DATE
python3 unique_list.py djde.bin juno.bin
python3 track_loader.py output.bin -d $RESULT_PATH -i $LOAD_IMG -s $DELAY -m $MAX_TRACKS
