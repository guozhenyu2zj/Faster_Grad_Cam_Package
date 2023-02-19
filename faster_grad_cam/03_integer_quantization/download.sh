#!/bin/bash

fileid="1RC3uWAqaHm5-Xzj6YbyM8xeQmcwD50TR"
html=`curl --proxy 127.0.0.1:7890 -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`
curl --proxy 127.0.0.1:7890 -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po '(confirm=[a-zA-Z0-9\-_]+)'`&id=${fileid}" -o weights_integer_quant.tflite

echo Download finished.
