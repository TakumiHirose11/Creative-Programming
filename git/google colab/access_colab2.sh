#!/bin/bash

for i in `seq 0 36`
do
  echo "[$i]" ` date '+%y/%m/%d %H:%M:%S'` "connected."
  open https://colab.research.google.com/drive/1IKUgpgeOFKH5B6Dm_TRJdzO8oo8bmQke#scrollTo=j_8UHvARgzji
  sleep 3600
done