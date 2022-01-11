#include <stdio.h>
#include "pcolparse.h"

int main(int argc, char **argv)
{

    if (argc != 2)
    {
        printf("Usage: %s [pathToLog]\n", argv[0]);
        return 1;
    }

    char *pathToLog = argv[1];

    struct Result result = parseAllIPPackets(pathToLog);
    struct IPPacket *packets = result.packets;

    printf("%s %s %u %u %u %i\n", packets[0].srcAddr, packets[0].dstAddr, packets[0].ihl, packets[0].totalLength, packets[0].data.dataOffset, result.count);
    return 0;
}