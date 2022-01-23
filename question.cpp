#include <fstream>
#include <iostream>
#include <string>

std::ifstream fin ("site_code.html");

int main() {
        char a;
        fin >> a;
        std::string str {};
        while (fin >> std::noskipws >> a)
        {
                str += a;
        }
        int index = str.find("student-session-question-title");
        int length {};
        for (int i = 0; i < str.size(); i++)
        {
                if (str[index + 33 + i] == '<')
                {
                        length = i + 1;
                        break;
                }
        }
        std::cout << "title: " << str.substr(index + 32, length) << "\n";
        fin.close();
        return 0;
}
