from flask import Flask, jsonify, render_template
import scapy.all as scapy
import threading

app = Flask(__name__)
captured_packets = []

def capture_packets():
    # Start capturing packets indefinitely
    scapy.sniff(prn=process_packet)

def process_packet(packet):
    packet_info = {
        "src": packet[scapy.IP].src if packet.haslayer(scapy.IP) else "N/A",
        "dst": packet[scapy.IP].dst if packet.haslayer(scapy.IP) else "N/A",
        "protocol": packet[scapy.IP].proto if packet.haslayer(scapy.IP) else "N/A",
        "summary": packet.summary()
    }
    # Append packet info to the global list
    captured_packets.append(packet_info)

@app.route('/api/packets')
def get_packets():
    # Serve captured packets as JSON
    return jsonify(captured_packets[-10:])  # Limit to the latest 10 packets for simplicity

@app.route('/')
def index():
    # Serve the HTML interface
    return render_template('index.html')

if __name__ == "__main__":
    # Start packet capturing in a separate thread to avoid blocking Flask
    capture_thread = threading.Thread(target=capture_packets)
    capture_thread.daemon = True
    capture_thread.start()

    # Run the Flask server
    app.run(host='0.0.0.0', port=5001)

