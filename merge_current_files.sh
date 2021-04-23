#!/bin/bash

cat horncurrents/*.txt > allhorncurrents.txt

echo 'date,current' | cat - allhorncurrents.txt > temp.txt; mv temp.txt allhorncurrents.txt
