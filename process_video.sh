#!/bin/bash

set -o errexit

rm -fr frames
mkdir frames
ffmpeg -i $1 -vsync 0 frames/frame%6d.png
