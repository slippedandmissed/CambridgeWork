#include <iostream>
#include <fstream>
#include "pcolparse.h"

int main(int argc, char **argv)
{

    if (argc != 3)
    {
        std::cout << "Usage: " << argv[0] << " [pathToLog] [pathToOutput]" << std::endl;
        return 1;
    }

    char *pathToLog = argv[1];
    char *pathToOutput = argv[2];

    auto packets = parseAllIPPackets(pathToLog);

    auto file = std::ofstream(pathToOutput);

    for (auto packet : packets) {
        file << packet.data.data;
    }

    file.close();

    return 0;
}