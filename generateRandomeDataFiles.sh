#!/bin/bash

generate_file() {
  size=$1
  filename="random_${size}.dat"
  dd if=/dev/urandom of="${filename}" bs="${size}" count=1
}

generate_file 100k
generate_file 500k
generate_file 1M
generate_file 5M
generate_file 10M
