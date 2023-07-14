#!/bin/bash

"""
This script decompose a video into frames
How to use: replace path_to_videos and path_to_frames with real paths
"""

for f in ./*.webm
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name\
  basename=$(ff=${f%.ext} ; echo ${ff##*/})
  name=$(echo "$basename" | cut -d'.' -f1)
  echo $f
  mkdir -p ./frames/$name
  echo "name =  $name"
  ffmpeg -i "$f" -f image2 -qscale:v 2 ./frames/$name/%06d.jpg
done
