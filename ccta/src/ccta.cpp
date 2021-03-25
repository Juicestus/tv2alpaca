/*
 * poster.cpp
 * A C++ version of my shitty test client for tv2alpaca (poster.py)
 * Just to practice C++ ig.
 * poster.py is still there for use.
 * Compile: g++ -std=c++11 -o poster poster.cpp -lcurl
 *      Use C++ >= 11 ^  ./poster ^    src ^      ^ libcurl
 * Have libcurl static library installed!
 * Mac:     $ brew install curl
 * Linux:   $ apt-get install curl
 * Windows: I don't fucking know lmfao
 */

#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <ctime>
#include <unistd.h>
#include <pwd.h>
#include <sys/types.h>
#include <curl/curl.h>

std::string home()
{
    std::string homestr;
    struct passwd *pw = getpwuid(getuid());
    const char *homedir = pw->pw_dir;
	homestr = homedir;
    return homestr;
}

std::string PATH = home() + "/.t2akeys";
std::string URL = "www.tv2alpaca.com";
std::string OPS[6] = {"--url","-u","--help","-h","--post","-p"};

char * stringToCharArr(std::string str)
{
    int n = str.length();
    char * chararr = NULL;
    chararr = new char[n+1];
 
    for (int i = 0; i < n; i++) 
    {
        chararr[i] = str[i];
    }    

    return chararr;
}

std::string stringfdto(std::time_t now,
				       std::string format = "%m-%d-%Y %H:%M:%S")
{
    struct tm ts;
    char buf[80];
    ts = *localtime(& now);
    strftime(buf, sizeof(buf), format.c_str(), &ts);
    return std::string(buf);
}

std::string datetime()
{
    auto rawTime = std::chrono::system_clock::now();
    std::time_t timeObj = std::chrono::system_clock::to_time_t(rawTime);
    std::string formatted = stringfdto(timeObj);
    return formatted;
}

bool argIs(std::string val, char *argv[], int index)
{
    if (std::strcmp(argv[index],val.c_str()) == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool stringInArgs(std::string val, char *argv[], int len)
{
    bool isIn = false;

    for (int i = 0; i < len; i++)
    {
        if(argv[i] == val) 
        {
            isIn = true;
        }
    }
    return isIn;
}

void write(std::string key, std::string secret, std::string path)
{
    std::ofstream file;
    file.open(path);
    file << key << "\n";
    file << secret;
    file.close();
}

std::string * read(std::string path) 
{
    static std::string keys[2];
        
    std::ifstream file;
    file.open(path);

    int i = 0;
    std::string ln = "";

    while (std::getline(file, ln)) 
    {
        keys[i] = ln;
        i++;
	}

    file.close();

    return keys;
}

void help()
{
    std::string msg = "tv2alpaca poster - by Justus Languell\n"
                       "Help & Usage\n"
                       "To set keys:\n"
                       "  setkeys <key> <secret> <filename>\n"
                       "  filename is optional ^ if left blank will\n"
                       "  default to \"" + PATH + "\"\n"
                       "To post order:\n"
                       "  post <side> <ticker> <contracts> <-p> <-u> \n"
                       "  -p : aka --path, set custom keypath, defval \"" 
                       + PATH + "\"\n"
                       "  -u : aka --url, set custom URL, defval \""
                       + URL + "\"\n"
                       "For help: -h or --help\n";

    std::cout << msg;
}

void request(std::string url, std::string req)
{
    CURL *curl;
    CURLcode res;
    std::string readBuffer;

    char *postthis = stringToCharArr(req);

    struct curl_slist *hs=NULL;
    hs = curl_slist_append(hs, "Content-Type: application/json");

    std::cout << "Posting: \n" << postthis << "\nTo:\n" << url << "\n";

    std::cout << "Response:\n";

    curl = curl_easy_init();
    if (curl) 
    {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, hs);
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS,postthis);
        res = curl_easy_perform(curl);

        if (res != CURLE_OK)
        {
            std::cout << "Warning: Curl failed!";
        }

        curl_easy_cleanup(curl);

        std::cout << readBuffer << "\n";
    }
} 

void post(std::string key, 
          std::string secret, 
          std::string url, 
          std::string side, 
          std::string ticker,
          std::string contracts)
{
    std::string sTime = datetime();

    std::string furl = "http://" 
                        + url 
                        + "/api/" 
                        + key 
                        + "/" 
                        + secret 
                        + "/endpoint";

    std::string body = "{\"side\":\"" 
                        + side 
                        + "\",\"ticker\":\""
                        + ticker 
                        + "\",\"size\":\""
                        + contracts
                        + "\",\"price\":\""
                        + "null"
                        + "\",\"sent\":\""
                        + sTime
                        + "\"}";

    request(furl, body);
}

void setKeys(std::string key, std::string secret, std::string path)
{
    std::cout << "Key:       " << key << "\n";
    std::cout << "Secret:    " << secret << "\n";
    std::cout << "Saved to:  " << path << "\n";

    write(key,secret,path);
}

std::string opArg(std::string param,
                  std::string abrv, 
                  char *argv[], 
                  int argc, 
                  std::string defval)
{
    std::string val = defval;

    if (argc > 3
    && (stringInArgs(abrv,argv,argc)
    || stringInArgs(param,argv,argc)))
    {
        for (int i=0; i < argc - 1; i++)
        {
            if (argIs(param,argv,i)
            || argIs(abrv,argv,i)) 
            {
                val = argv[i+1];
            }
            
        }
    }

    return val;
}

int main(int argc, char **argv) 
{
    if (argc > 1) 
    {
        if (stringInArgs("-h",argv,argc) 
        || stringInArgs("--help",argv,argc))
        {
            help();
        }
        else 
        {
            if (argIs("setkeys",argv,1)) 
            {
                if (argc > 3)
                {   
                    std::string path = PATH;
                    if (argc > 4) 
                    {
                        path = argv[4];
                    }
                    setKeys(argv[2],argv[3],path);
                }
            }

            else if (argIs("post",argv,1)) 
            {
                std::string path = opArg("--path",
                                        "-p",
                                        argv,
                                        argc,
                                        PATH);

                std::string url = opArg("--url",
                                        "-u",
                                        argv,
                                        argc,
                                        URL);

                std::string *keys;
                keys = read(path);

                bool opInRes = false;

                for (int i = 0; i < 6; i++)
                {
                    std::string op = OPS[i];
                    
                    for (int j = 0; j < 5; j++)
                    {
                        if (argIs(op,argv,j))
                        {
                            opInRes = true;
                        }
                    }
                }

                if (!opInRes)
                {
                    post(keys[0], 
                    keys[1], 
                    url, 
                    argv[2], 
                    argv[3], 
                    argv[4]);
                }
                else
                {
                    std::cout << "Warning: Optional args must go "
								 "after required args!\n";
                }
                
            }
        }
    }
    else
    {
        std::cout << "Please provide args! -h for help.\n";
    }
}