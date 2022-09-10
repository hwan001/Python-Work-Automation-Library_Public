import sys
import subprocess

try:
    from ipaddress import IPv4Network
    from socket import *
    from struct import pack, unpack
    from requests import head

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])

import config


# 테스트
def getChksum(header):
    checksum = 0
    if(len(header) % 2) == 1:
        header += b'\x00'
    header = unpack(str(len(header)//2) +'H', header)
    for x in header:
        checksum+=x
    checksum += (checksum >> 16)
    checksum = (checksum & 0xFFFF) ^ 0xFFFF
    return checksum
    
# 테스트
def ping():
    sock =  socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
    
    data = "hello".encode()
    header = pack("bbHHh", 8, 0, 0, 1, 1)
    checksum = getChksum(header+data)
    packet = pack("bbHHh", 8, 0, checksum, 1, 1) + data
    for i in range(0, 255):
        tmp_ip = "172.20.13.%s" % i
        print(tmp_ip)
        sock.sendto(packet, (tmp_ip, 0))
        

    
    