#!/bin/bash

set -o errexit

frame=$(echo $1 | grep --only-matching --perl-regexp '[1-9]\d*')
convert $1 -format "Frame: $frame Client: %[pixel:p{$2,$3}] Host: %[pixel:p{$4,$5}]\n" info:
