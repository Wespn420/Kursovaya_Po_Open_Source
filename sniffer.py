from flask import Flask, jsonify
from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP, ICMP
from threading import Thread
import queue

sniffer = Flask(__name__)
packet_queue = queue.Queue()

def packet_callback(packet):
    if IP in packet:
        packet_data = {
            "protocol": packet[IP].proto,
            "src_ip": packet[IP].src,
            "dst_ip": packet[IP].dst
        }

        if TCP in packet:
            packet_data["protocol_name"] = "TCP"
            packet_data["src_port"] = packet[TCP].sport
            packet_data["dst_port"] = packet[TCP].dport
        
        elif UDP in packet:
            packet_data["protocol_name"] = "UDP"
            packet_data["src_port"] = packet[UDP].sport
            packet_data["dst_port"] = packet[UDP].dport

        elif ICMP in packet:
            packet_data["protocol_name"] = "ICMP"
            packet_data["icmp_type"] = packet[ICMP].type
            packet_data["icmp_code"] = packet[ICMP].code

        else:
            packet_data["protocol_name"] = "Неизвестный протокол"

        packet_queue.put(packet_data)

def start_sniffing():
    sniff(prn=packet_callback, filter="ip", store=0)    

@sniffer.route("/packets", methods=["GET"])
def get_packets():
    packets = []
    while not packet_queue.empty():
        packets.append(packet_queue.get())
    return jsonify(packets)

if __name__ == "__main__":
    sniff_thread = Thread(target=start_sniffing, daemon=True)
    sniff_thread.start()
    sniffer.run(debug=True)
