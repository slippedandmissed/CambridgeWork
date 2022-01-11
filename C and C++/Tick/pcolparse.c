#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "pcolparse.h"

unsigned int readUintFromFile(FILE *file, unsigned int count)
{
    // NOTE: big endian
    int size = sizeof(char) * (count + 1);
    char *buf = (char *)malloc(size);
    fgets(buf, count + 1, file);
    unsigned int result = 0;
    for (unsigned int i = 0; i < count; i++)
    {
        result = (result << 8 * sizeof(char)) + ((unsigned char)buf[i]);
    }
    return result;
}

unsigned int readUintFromCharArray(char *buf, unsigned int start, unsigned int end)
{
    // NOTE: big endian, [start,end)
    unsigned int result = 0;
    for (unsigned int i = start; i < end; i++)
    {
        result = (result << 8 * sizeof(char)) + ((unsigned char)buf[i]);
    }
    return result;
}

struct TCPPacket parseTCPPacket(char *buf, int length)
{
    struct TCPPacket packet;
    packet.srcPort = readUintFromCharArray(buf, 0, 2);
    packet.dstPort = readUintFromCharArray(buf, 2, 4);
    packet.seq = readUintFromCharArray(buf, 4, 8);
    packet.ack = readUintFromCharArray(buf, 8, 12);
    packet.dataOffset = ((unsigned char)buf[12]) >> 4;
    packet.reserved = (readUintFromCharArray(buf, 12, 14) >> 6) & 63;
    packet.controlBits = readUintFromCharArray(buf, 12, 14) & 63;
    packet.window = readUintFromCharArray(buf, 14, 16);
    packet.checksum = readUintFromCharArray(buf, 16, 18);
    packet.urgentPtr = readUintFromCharArray(buf, 18, 20);

    int dataStartIndex = 4 * (packet.dataOffset);
    packet.dataLength = length - dataStartIndex;

    packet.data = (char *)malloc(sizeof(char) * packet.dataLength);

    memcpy(packet.data, buf + dataStartIndex, sizeof(char) * packet.dataLength);

    return packet;
}

struct IPPacket *parseIPPacket(FILE *file)
{
    fgetc(file);
    if (feof(file))
    {
        return NULL;
    }
    fseek(file, -1, SEEK_CUR);
    int startIndex = ftell(file);
    unsigned int versionAndIHL = readUintFromFile(file, 1);
    struct IPPacket *packet = malloc(sizeof(struct IPPacket));
    packet->version = versionAndIHL >> 4;
    packet->ihl = versionAndIHL & 15;
    packet->typeOfService = readUintFromFile(file, 1);
    packet->totalLength = readUintFromFile(file, 2);
    packet->identification = readUintFromFile(file, 2);
    unsigned int flagsAndFragmentOffset = readUintFromFile(file, 2);
    packet->flags = flagsAndFragmentOffset >> 13;
    packet->fragmentOffset = flagsAndFragmentOffset & 8191;
    packet->ttl = readUintFromFile(file, 1);
    packet->protocol = readUintFromFile(file, 1);
    packet->headerChecksum = readUintFromFile(file, 2);

    packet->srcAddr = (char *)malloc(16 * sizeof(char));
    packet->dstAddr = (char *)malloc(16 * sizeof(char));

    int srcLen = 0;
    int dstLen = 0;

    for (int i = 0; i < 4; i++)
    {
        srcLen += sprintf(packet->srcAddr + srcLen, i == 0 ? "%u" : ".%u", readUintFromFile(file, 1)) / sizeof(char);
    }
    for (int i = 0; i < 4; i++)
    {
        dstLen += sprintf(packet->dstAddr + dstLen, i == 0 ? "%u" : ".%u", readUintFromFile(file, 1)) / sizeof(char);
    }

    fseek(file, 4 * packet->ihl + startIndex, SEEK_SET);
    int dataLen = packet->totalLength - 4 * packet->ihl;
    char *dataBuf = (char *)malloc((dataLen + 1) * sizeof(char));
    fread(dataBuf, sizeof(char), dataLen, file);
    packet->data = parseTCPPacket(dataBuf, dataLen);

    fseek(file, packet->totalLength + startIndex, SEEK_SET);

    return packet;
}

struct Result parseAllIPPackets(char *path)
{
    FILE *file;
    file = fopen(path, "r");

    struct IPPacket *packetPtrs[1024];
    int len = 0;

    struct IPPacket *ip;
    while ((ip = parseIPPacket(file)) != NULL)
    {
        packetPtrs[len++] = ip;
    }

    struct Result result;
    result.count = len;
    result.packets = (struct IPPacket *)malloc(sizeof(struct IPPacket) * len);
    for (int i = 0; i < len; i++)
    {
        result.packets[i] = *(packetPtrs[i]);
        free(packetPtrs[i]);
    }

    fclose(file);

    return result;
}