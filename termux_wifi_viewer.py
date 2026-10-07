import os
import re

BANNER = """

   📱 Termux WiFi Password Viewer
   For ROOTED Android Only

"""

def check_root():
    if os.geteuid() != 0:
        print("[-] Error: Root permission required!")
        print("[*] Run: su -c 'python termux_wifi_viewer.py'")
        return False
    return True

def get_wifi_passwords():
    wifi_file = "/data/misc/wifi/wpa_supplicant.conf"
    
    try:
        with open(wifi_file, "r") as f:
            data = f.read()
    except PermissionError:
        print("[-] Permission Denied! Run with root: su")
        return
    except FileNotFoundError:
        print("[-] File not found! Is your phone rooted?")
        return

    networks = re.findall(r'network={([^}]+)}', data)
    
    if not networks:
        print("[-] No saved WiFi found!")
        return
        
    print(f"\n[+] Found {len(networks)} WiFi networks:\n")
    print("-"*40)
    
    for i, net in enumerate(networks, 1):
        ssid = re.search(r'ssid="(.+?)"', net)
        psk = re.search(r'psk="(.+?)"', net)
        
        ssid = ssid.group(1) if ssid else "Hidden"
        psk = psk.group(1) if psk else "No Password / EAP"
        
        print(f"[{i}] SSID : {ssid}")
        print(f"    Pass : {psk}")
        print("-"*40)

def main():
    print(BANNER)
    if check_root():
        get_wifi_passwords()

if __name__ == "__main__":
    main()
