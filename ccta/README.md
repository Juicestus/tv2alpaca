# CCTA
### C++ Curl to Alpaca
### [tv2alpaca](http://tv2alpaca.com/) C++ Test Client for submitting post requests
## Install
Make sure you have [LibCURL](https://curl.se/libcurl/).\
If libcurl.a is at a specific path, put that instead of -lcurl I think.\
How to install basically:
 * Mac:      ```brew install curl```
 * Linux:    ```apt-get install curl```
 * Windows: I don't fucking know lmfao

On unix, in this dir, run:\
```g++ -std=c++11 -o bin/ccta src/ccta.cpp -lcurl```\
to compile and save the binary in bin.\
If you want to use it from local binaries, run\
```mv bin/ccta /usr/local/bin```
## Use
To run, use ```./bin/ccta``` + args or ```ccta``` + args if running from local binaries. \
Run ```ccta -h``` for a list of actions and use.\
To enter your keys, run ```ccta setkeys <keyid> <secret>```\
To make a post to the server, run ```ccta post <buy/sell> <ticker> <contracts>```\
Optional args for post are:
 * ```-p/--path```: a custom path for keys
 * ```-u/--url```: a URL to post to
