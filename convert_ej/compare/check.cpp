#include "testlib.h"
#include <string>
#include <vector>
#include <sstream>

using namespace std;

string ending(int x)
{
    x %= 100;
    if (x / 10 == 1)
        return "th";
    if (x % 10 == 1)
        return "st";
    if (x % 10 == 2)
        return "nd";
    if (x % 10 == 3)
        return "rd";
    return "th";
}

int main(int argc, char * argv[])
{
    setName("compare files as sequence of lines");
    registerTestlibCmd(argc, argv);

    std::string strAnswer;

    int n = 0;
    while (!ans.eof()) 
    {
        std::string j = ans.readString();

        if (j == "" && ans.eof())
            break;

        strAnswer = j;
      
        std::string p = ouf.readString();

        n++;

        // disregard spaces
        string jNoSpaces;
        for(auto c: j) if(c!=' ')
            jNoSpaces.push_back(c);
        string pNoSpaces;
        for(auto c: p) if(c!=' ')
            pNoSpaces.push_back(c);

        // lowercase the strings
        for(auto &c: jNoSpaces)
            c = tolower(c);
        for(auto &c: pNoSpaces)
            c = tolower(c);

        if (jNoSpaces != pNoSpaces)
            quitf(_wa, "%d%s lines differ - expected: '%s', found: '%s'", n, ending(n).c_str(), j.c_str(), p.c_str());
    }
    
    if (n == 1 && strAnswer.length() <= 128)
        quitf(_ok, "%s", strAnswer.c_str());

    quitf(_ok, "%d lines", n);
}