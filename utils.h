#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <regex>

namespace Utils
{
    std::string getChapterURL(std::string baseURL, int chapNum);
    std::string getFilenameChapter(std::string ficName, std::string chap_url);
    std::string unixdFicName(std::string ficName);

}
#endif // UTILS_H
