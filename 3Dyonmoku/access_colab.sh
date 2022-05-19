#!/bin/bash

for i in `seq 0 36`
do
  echo "[$i]" ` date '+%y/%m/%d %H:%M:%S'` "connected."
  open https://colab.research.google.com/drive/1ewyVeD2JPi9lMeu5HrS1Q_5YKMSXjlLI#scrollTo=mIykYMr9KGiA
  sleep 3600
done