#pragma once

struct TCPPacket
{
    unsigned int srcPort;
    unsigned int dstPort;
    unsigned int seq;
    unsigned int ack;
    unsigned int dataOffset;
    unsigned int reserved;
    unsigned int controlBits;
    unsigned int window;
    unsigned int checksum;
    unsigned int urgentPtr;
    char *data;
    int dataLength;
};

struct IPPacket
{
    unsigned int version;
    unsigned int ihl;
    unsigned int typeOfService;
    unsigned int totalLength;
    unsigned int identification;
    unsigned int flags;
    unsigned int fragmentOffset;
    unsigned int ttl;
    unsigned int protocol;
    unsigned int headerChecksum;
    char *srcAddr;
    char *dstAddr;
    struct TCPPacket data;
};

struct Result
{
    struct IPPacket *packets;
    int count;
};

struct Result parseAllIPPackets(char *path);