# CCTA
### C++ Curl to Alpaca
### tv2alpaca C++ Test Client for submitting post requests
## Install
Make sure you have (LibCURL)[https://curl.se/libcurl/].\
If libcurl.a is at a specific path, put that instead of -lcurl I think.\
How to install basically:
 * Mac:     $ brew install curl
 * Linux:   $ apt-get install curl
 * Windows: I don't fucking know lmfao

On unix, in this dir, run:\
```$ g++ -std=c++11 -o bin/poster src/poster.cpp -lcurl```\
to compile and save the binary in bin.

