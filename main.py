import netaddr
import os
from config import (TR_IPBLOCKS, LOAD_FILE, OUTPUT_TR, OUTPUT_OTHERS)
IPLIST = []
TURKISH_IPS = []
OTHER_IPS = []

if not os.path.exists(LOAD_FILE):
    print(f"{LOAD_FILE} not found.")
    exit()

def is_valid_ip(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True

load = open(LOAD_FILE,"r")
loadInfo = load.readlines()
load.close()

for ip in loadInfo:
    ipCleared = ip.replace("\n", "").strip()
    if is_valid_ip(ipCleared) is False:
        continue
    IPLIST.append(ipCleared)

print(f"{str(len(IPLIST))} IP(s) loaded.\nFiltering IP list...")

for ip in IPLIST:
    ipDecimal = int(netaddr.IPAddress(ip))
    stop = False
    for ipBlock in TR_IPBLOCKS:
        if is_valid_ip(ipBlock[0]) is False or is_valid_ip(ipBlock[1]) is False:
            continue
        startBlockDecimal = int(netaddr.IPAddress(ipBlock[0]))
        endBlockDecimal = int(netaddr.IPAddress(ipBlock[1]))
        if ipDecimal >= startBlockDecimal and ipDecimal <= endBlockDecimal:
            TURKISH_IPS.append(ip)
            stop = True
            continue
    if stop is True:
        continue
    OTHER_IPS.append(ip)

tr_output = open(OUTPUT_TR, "w")
tr_output.write("\n".join(TURKISH_IPS))
tr_output.close()
print(f"\n== TURKISH IP LIST ==\nSaved to {OUTPUT_TR} ({len(TURKISH_IPS)})")

other_output = open(OUTPUT_OTHERS, "w")
other_output.write("\n".join(OTHER_IPS))
other_output.close()
print(f"\n== OTHER IP LIST ==\nSaved to {OUTPUT_OTHERS} ({len(OTHER_IPS)})")