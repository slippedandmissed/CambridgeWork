#include <iostream>
#include "pcolparse.h"

int main(int argc, char **argv)
{

    if (argc != 2)
    {
        std::cout << "Usage: " << argv[0] << " [pathToLog]" << std::endl;
        return 1;
    }

    char *pathToLog = argv[1];

    auto packets = parseAllIPPackets(pathToLog);

    std::cout << packets.at(0).srcAddr << " " << packets.at(0).dstAddr << " " << packets.at(0).ihl << " " << packets.at(0).totalLength << " " << packets.at(0).data.dataOffset << " " << packets.size() << std::endl;

    return 0;
}