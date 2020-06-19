#include "utils.h"

namespace Utils
{

std::string getChapterURL(std::string baseURL, int chapNum)
{
    // sample URL: https://www.fanfiction.net/s/2803341/1/Accounting-no-Jutsu

    //NOTABENE unicode considerations?
    int nameDivider = baseURL.rfind("/");
    baseURL = baseURL.substr(0, nameDivider);
    int chapDivider = baseURL.rfind("/");
    baseURL = baseURL.substr(0, chapDivider+1); //include slash too

    return baseURL + std::to_string(chapNum);

}

std::string getFilenameChapter(std::string ficName, std::string chap_url)
{
    //https://www.fanfiction.net/s/2803341/1
    //Accounting_no_Jutsu__Chap_1
    int ind = chap_url.rfind("/");
    return unixdFicName(ficName) + "__" + "Chap_" + chap_url.substr(ind, chap_url.length()) + ".html";

}

std::string unixdFicName(std::string ficName)
{
    // sample: "Accounting no Jutsu's Reboot"
    std::string unixedName;

    for (char c : ficName) {
        if (c == ' ') {
            unixedName += '_';
            continue;
        } else if (c == '\'') {
            unixedName += "_";
            continue;
        }
        unixedName += c;

    }

    return unixedName;
}

} //END_NAMESPACE_Utils
