#!/bin/bash
echo "If it says file exists just ignore it lol"
mkdir bin
g++ -std=c++11 -o bin/poster src/poster.cpp -lcurl
#mv bin/poster /usr/local/bin
echo "Build successful!"
