#!/bin/bash

for i in `seq 0 36`
do
  echo "[$i]" ` date '+%y/%m/%d %H:%M:%S'` "connected."
  open https://colab.research.google.com/drive/1CZyLq0e2KlI90HA17PTMx_rA_QavOqxo#scrollTo=zFJo4mrfw9p9
  sleep 3600
done