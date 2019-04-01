#!/bin/bash

set -o errexit

ls frames |
  sort |
  parallel --keep-order --will-cite ./process_frame.sh frames/{} $1 $2 $3 $4 > colors
