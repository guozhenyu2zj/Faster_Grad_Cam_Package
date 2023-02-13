#!/bin/bash

fileid="1vPPCnOXBSpplElCQKUJ6-EhjDVmpFOND"
html=`curl --proxy 127.0.0.1:7890 -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`
curl --proxy 127.0.0.1:7890 -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po '(confirm=[a-zA-Z0-9\-_]+)'`&id=${fileid}" -o resources.tar.gz
tar -zxvf resources.tar.gz
rm resources.tar.gz

echo Download finished.
