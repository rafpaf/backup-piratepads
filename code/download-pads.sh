#!/bin/bash
for url in `cat pad_urls`; do
    wget "http://piratepad.net/ep/pad/export/$url/latest?format=html" -O "$url.html"
done
cd `dirname $0`
git add *.html
git commit -m "automatic commit by code/download-pads.sh"
