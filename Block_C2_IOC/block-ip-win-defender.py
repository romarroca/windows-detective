import requests
import subprocess
import re
import ipaddress
import csv
from tqdm import tqdm

def is_valid_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def fetch_ip_list(url):
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.strip().split('\n')
        valid_ips = []
        for line in lines:
            line = line.strip()  # Remove any extraneous whitespace
            if not line.startswith("#"):
                #print(f"Checking line: '{line}'")  # Debug print
                if is_valid_ipv4(line):
                    #print(f"Valid IP: '{line}'")  # Debug print
                    valid_ips.append(line)
        return valid_ips
    else:
        print("Failed to download IP list")
        return []

def save_ips_to_csv(ip_list, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for ip in ip_list:
            writer.writerow([ip])

def load_ips_from_csv(filename):
    ip_list = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            ip_list.append(row[0])
    return ip_list

def delete_rules(ip_list, rule_prefix):
    for ip in tqdm(ip_list, desc='Deleting Rules'):
        for direction in ['in', 'out']:
            rule_name = f"{rule_prefix}_{direction}_{ip}"
            cmd = f"netsh advfirewall firewall delete rule name=\"{rule_name}\""
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_initial_rule(ip):
    rule_name = "AutoBlock_Rule"
    for direction in ["in", "out"]:
        command = f"netsh advfirewall firewall add rule name=\"{rule_name}_{direction}_{ip}\" dir={direction} action=block"
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def block_ip(ip):
    rule_name = "AutoBlock_Rule"
    for direction in ["in", "out"]:
        command = f"netsh advfirewall firewall set rule name=\"{rule_name}_{direction}_{ip}\" new remoteip={ip}"
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":

    print("""
          Hey there! This script is designed to block connections that are either destined for or 
          originating from Botnet C2 Indicators of Compromise (IOCs) from the past 30 days. 
          You can verify the source data at "https://feodotracker.abuse.ch/blocklist/"

          Disclaimer: I use this script personally as an additional layer of security for my 
          computer. While it aims to enhance security, it is not a guaranteed 
          solution for protecting your PC. Use this script at your own risk and discretion. 
          Make sure you understand its functionality before implementing it.

          """)
    action = input("Do you want to 'block', or 'unblock' IPs? (Type 'block', or 'unblock'): ").lower()

    if action == 'block':
        url = "https://feodotracker.abuse.ch/downloads/ipblocklist.txt"
        ip_list = fetch_ip_list(url)
        save_ips_to_csv(ip_list, 'blocked_ips.csv')
        for ip in tqdm(ip_list, desc='Blocking IPs'):
            #print(f"Blocking {ip}") # Debug print
            create_initial_rule(ip)
            block_ip(ip)
    elif action == 'unblock':
        ip_list = load_ips_from_csv('blocked_ips.csv')
        delete_rules(ip_list, 'AutoBlock_Rule')
    else:
        print("Invalid action. Exiting.")
