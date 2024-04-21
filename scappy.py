from scapy.all import *
from scapy.arch.windows import conf

def packet_handler(pkt):
    if pkt.haslayer(Dot11):  # Check if the packet is a WiFi packet
        if pkt.type == 0 and pkt.subtype == 8:  # Check if it's a data packet
            print("Received WiFi data packet:")
            print(pkt.summary())

# Set the default socket to be L3 socket (Layer 3)
conf.L3socket

# Start sniffing WiFi packets on the specified interface
# Change 'wlan0' to your WiFi interface name
sniff(iface="wlan0", prn=packet_handler)