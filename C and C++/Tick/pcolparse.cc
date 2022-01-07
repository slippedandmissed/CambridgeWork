#include <fstream>
#include <cstring>
#include <vector>
#include <string>
#include "pcolparse.h"

uint readUintFromFile(std::ifstream *file, uint count)
{
    // NOTE: big endian
    auto buf = new char[count];
    file->read(buf, count);
    uint result = 0;
    for (uint i = 0; i < count; i++)
    {
        result = (result << 8 * sizeof(char)) + ((u_char)buf[i]);
    }
    return result;
}

uint readUintFromCharArray(char *buf, uint start, uint end)
{
    // NOTE: big endian, [start,end)
    uint result = 0;
    for (uint i = start; i < end; i++)
    {
        result = (result << 8 * sizeof(char)) + ((u_char)buf[i]);
    }
    return result;
}

TCPPacket parseTCPPacket(char *buf, int length)
{
    TCPPacket packet;

    packet.srcPort = readUintFromCharArray(buf, 0, 2);
    packet.dstPort = readUintFromCharArray(buf, 2, 4);
    packet.seq = readUintFromCharArray(buf, 4, 8);
    packet.ack = readUintFromCharArray(buf, 8, 12);
    packet.dataOffset = ((u_char) buf[12]) >> 4;
    packet.reserved = (readUintFromCharArray(buf, 12, 14) >> 6) & 63;
    packet.controlBits = readUintFromCharArray(buf, 12, 14) & 63;
    packet.window = readUintFromCharArray(buf, 14, 16);
    packet.checksum = readUintFromCharArray(buf, 16, 18);
    packet.urgentPtr = readUintFromCharArray(buf, 18, 20);

    int dataStartIndex = 4 * (packet.dataOffset);
    int dataLength = length - dataStartIndex;
    packet.data = std::string(buf + dataStartIndex, dataLength);

    return packet;
}

IPPacket *parseIPPacket(std::ifstream *file)
{
    auto startIndex = file->tellg();
    auto packet = new IPPacket();
    auto versionAndIHL = readUintFromFile(file, 1);
    packet->version = versionAndIHL >> 4;
    packet->ihl = versionAndIHL & 15;
    packet->typeOfService = readUintFromFile(file, 1);
    packet->totalLength = readUintFromFile(file, 2);
    packet->identification = readUintFromFile(file, 2);
    auto flagsAndFragmentOffset = readUintFromFile(file, 2);
    packet->flags = flagsAndFragmentOffset >> 13;
    packet->fragmentOffset = flagsAndFragmentOffset & 8191;
    packet->ttl = readUintFromFile(file, 1);
    packet->protocol = readUintFromFile(file, 1);
    packet->headerChecksum = readUintFromFile(file, 2);

    packet->srcAddr = new char[16];
    packet->dstAddr = new char[16];
    for (int i = 0; i < 4; i++)
    {
        std::sprintf(packet->srcAddr + strlen(packet->srcAddr), i == 0 ? "%u" : ".%u", readUintFromFile(file, 1));
    }
    for (int i = 0; i < 4; i++)
    {
        std::sprintf(packet->dstAddr + strlen(packet->dstAddr), i == 0 ? "%u" : ".%u", readUintFromFile(file, 1));
    }

    file->seekg(4 * packet->ihl + startIndex, file->beg);
    auto dataLen = packet->totalLength - 4 * packet->ihl;
    auto dataBuf = new char[dataLen];
    file->read(dataBuf, dataLen);
    packet->data = parseTCPPacket(dataBuf, dataLen);

    file->seekg(packet->totalLength + startIndex, file->beg);
    if (!(file->good()))
    {
        return nullptr;
    }

    return packet;
}

std::vector<IPPacket> parseAllIPPackets(char *path)
{
    auto file = new std::ifstream(path);
    std::vector<IPPacket> packets;
    IPPacket *ip;
    while ((ip = parseIPPacket(file)) != nullptr)
    {
        packets.push_back(*ip);
        delete ip;
    }
    file->close();

    return packets;
}