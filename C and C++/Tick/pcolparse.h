#pragma once

#include <vector>

struct TCPPacket
{
    uint srcPort;
    uint dstPort;
    uint seq;
    uint ack;
    uint dataOffset;
    uint reserved;
    uint controlBits;
    uint window;
    uint checksum;
    uint urgentPtr;
    std::string data;
};

struct IPPacket
{
    uint version;
    uint ihl;
    uint typeOfService;
    uint totalLength;
    uint identification;
    uint flags;
    uint fragmentOffset;
    uint ttl;
    uint protocol;
    uint headerChecksum;
    char *srcAddr;
    char *dstAddr;
    TCPPacket data;
};

std::vector<IPPacket> parseAllIPPackets(char *path);