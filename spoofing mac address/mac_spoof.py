import subprocess
import re

def get_current_mac(interface):
    result = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
    match = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", result.stdout)
    if match:
        return match.group(0)
    else:
        print("Could not read MAC address.")
        return None

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.run(["sudo", "ifconfig", interface, "down"])
    subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["sudo", "ifconfig", interface, "up"])

    current_mac = get_current_mac(interface)
    if current_mac == new_mac:
        print(f"[+] MAC address successfully changed to {current_mac}")
    else:
        print("[-] MAC address did not get changed.")

interface = "eth0"  # Change this to your network interface (e.g., wlan0 for Wi-Fi)
new_mac = "00:11:22:33:44:55"  # Change to your desired MAC address

print(f"Current MAC: {get_current_mac(interface)}")
change_mac(interface, new_mac)
print(f"Updated MAC: {get_current_mac(interface)}")
