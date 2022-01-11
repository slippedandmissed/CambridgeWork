#include <iostream>
#include <fstream>

extern "C"
{
#include "pcolparse.h"
}

int main(int argc, char **argv)
{

    if (argc != 3)
    {
        std::cout << "Usage: " << argv[0] << " [pathToLog] [pathToOutput]" << std::endl;
        return 1;
    }

    char *pathToLog = argv[1];
    char *pathToOutput = argv[2];

    Result result = parseAllIPPackets(pathToLog);

    auto file = std::ofstream(pathToOutput);

    for (int i = 0; i < result.count; i++)
    {
        for (int j = 0; j < result.packets[i].data.dataLength; j++)
        {
            file << result.packets[i].data.data[j];
        }
    }

    file.close();

    return 0;
}