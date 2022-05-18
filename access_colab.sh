#!/bin/bash

for i in `seq 0 36`
do
  echo "[$i]" ` date '+%y/%m/%d %H:%M:%S'` "connected."
  open https://colab.research.google.com/drive/179m_UKTjUDfHqG_cyviiXGgWxNMnTFyU?hl=ja#scrollTo=6K5myHAO5YE4
  sleep 3600
done