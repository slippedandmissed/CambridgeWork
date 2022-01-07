#!/usr/bin/python3.9
import sys

if len(sys.argv) < 2:
    print("Usage: fiddle [filename]")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "rb") as file:
    data = file.read()


def load_tcp_packet(packet):
    result = {
        "header": {
            "src_port": int.from_bytes(packet[:2], "big"),
            "dst_port": int.from_bytes(packet[2:4], "big"),
            "seq": int.from_bytes(packet[4:8], "big"),
            "ack": int.from_bytes(packet[8:12], "big")
        },
        "data_offset": packet[12] >> 4,
        "reserved": (int.from_bytes(packet[12:14], "big") >> 6) & 0b111111,
        "control_bits": int.from_bytes(packet[12:14], "big") & 0b111111,
        "window": int.from_bytes(packet[14:16], "big"),
        "checksum": int.from_bytes(packet[16:18], "big"),
        "urgent_ptr": int.from_bytes(packet[18:20], "big")
    }

    result["data"] = packet[4*result["data_offset"]:]

    return result

def load_ip_packets(packet):
    if len(packet) == 0:
        return []
    result = {
        "header": {
            "version": packet[0] >> 4,
            "ihl": packet[0] & 0b1111,
            "type_of_service": packet[1],
            "total_length": int.from_bytes(packet[2:4], "big"),
            "identification": int.from_bytes(packet[4:6], "big"),
            "flags": packet[6] >> 5,
            "fragment_offset": int.from_bytes(packet[6:8], "big") & 0b1111111111111,
            "ttl": packet[8],
            "protocol": packet[9],
            "header_checksum": int.from_bytes(packet[10:12], "big"),
            "src_addr": ".".join(str(i) for i in packet[12:16]),
            "dst_addr": ".".join(str(i) for i in packet[16:20])
        }
    }

    result["data"] = packet[4*result["header"]["ihl"]:result["header"]["total_length"]]

    rest = packet[result["header"]["total_length"]:]

    return [result]+load_ip_packets(rest)


ip = load_ip_packets(data)
print(ip[0]["header"]["src_addr"], end=" ")
print(ip[0]["header"]["dst_addr"], end=" ")
print(ip[0]["header"]["ihl"], end=" ")
print(ip[0]["header"]["total_length"], end=" ")

tcp = load_tcp_packet(ip[0]["data"])
print(tcp["data_offset"], end=" ")
print(len(ip))