import subprocess
import re
import socket
import requests
import json
from tqdm import tqdm
from geolite2 import geolite2
import whois

def read_public_ips(filename="public_network_connections.txt"):
    with open(filename, "r") as f:
        return set(line.strip() for line in f)

def check_ip_reputation(ip, api_key, all_ip_data):
    headers = {'Key': api_key}
    params = {'maxAgeInDays': 90, 'ipAddress': ip}
    try:
        response = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params)
        data = response.json()
        all_ip_data[ip] = data
        if 'data' in data and 'abuseConfidenceScore' in data['data']:
            return data['data']['abuseConfidenceScore']
        else:
            return "No abuse score available"
    except Exception as e:
        return f"Could not check IP reputation: {e}"

def write_to_json_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def get_geoip(ip):
    reader = geolite2.reader()
    location = reader.get(ip)
    geolite2.close()
    if location and 'country' in location:
        return location['country']['iso_code']
    return 'Unknown'

def get_whois(ip):
    try:
        w = whois.whois(ip)
        return w.org or w.owner or 'Unknown'
    except:
        return 'Unknown'

def gather_info_on_ip(ip, api_key, all_ip_data):
    try:
        resolved_name = socket.gethostbyaddr(ip)
        print(f"{ip} resolves to {resolved_name[0]}")
    except socket.herror:
        print(f"{ip} could not be resolved")
        
    country = get_geoip(ip)
    print(f"  Country: {country}")

    who = get_whois(ip)
    print(f"  Organization: {who}")

    abuse_score = check_ip_reputation(ip, api_key, all_ip_data)
    print(f"  Abuse Score: {abuse_score}")

def check_network_connections():
    result = subprocess.run("netstat -ano", shell=True, capture_output=True, text=True)
    netstat_output = result.stdout

    pattern = re.compile(r'\d+\.\d+\.\d+\.\d+:\d+\s+(\d+\.\d+\.\d+\.\d+:\d+)\s+\w+\s+(\d+)', re.MULTILINE)
    matches = pattern.findall(netstat_output)
    public_ip_pid_map = {}
    filtered_ip_reasons = {}

    for ip, pid in matches:
        octets = ip.split(":")[0].split(".")
        reason = "Public"
        if octets[0] == "127":
            reason = "Localhost"
        elif octets[0] == "0":
            reason = "Unspecified"
        elif octets[0] == "10":
            reason = "Private (10.x.x.x)"
        elif octets[0] == "192" and octets[1] == "168":
            reason = "Private (192.168.x.x)"
        elif octets[0] == "172" and 16 <= int(octets[1]) <= 31:
            reason = "Private (172.16-31.x.x)"
        
        if reason == "Public":
            public_ip_pid_map[ip] = pid
        else:
            filtered_ip_reasons[ip] = reason

    with open("public_network_connections.txt", "w") as f:
        for ip, pid in public_ip_pid_map.items():
            f.write(f"{ip} {pid}\n")


def check_abuse_of_public_ips(api_key):
    all_ip_data = {}
    summary = {}
    public_ip_pid_map = {}

    with open("public_network_connections.txt", "r") as f:
        for line in f:
            ip_port, pid = line.strip().split()
            ip = ip_port.split(":")[0]  # Separate the IP from the port
            public_ip_pid_map[ip] = pid

    print("Checking IP reputations...")
    for ip, pid in tqdm(public_ip_pid_map.items()):
        abuse_score = check_ip_reputation(ip, api_key, all_ip_data)
        geo_info = get_geoip(ip)
        who_info = get_whois(ip)

        summary[ip] = {'PID': pid, 'Abuse Score': abuse_score, 'Geolocation': geo_info, 'Organization': who_info}

    # Save JSON data
    write_to_json_file(all_ip_data, "all_ip_reputations.json")

    # Print the summary
    print("\nHere's the juicy info we've got:")
    for ip, data in summary.items():
        print(f"IP Address: {ip}")
        for key, value in data.items():
            print(f"  {key}: {value}")


    
if __name__ == "__main__":
    print("=" * 60)
    print("            Network Detective Script!")
    print("=" * 60)
    print("Sure, you've got antivirus, but do you really know who your computer's chatting with?")
    print("\nSo, what's this script gonna do for you?")
    print("1. Check on who your computer is talking to right now.")
    print("2. Snoop around and tell you where these IPs are from and who might own them.")
    print("3. Give you the lowdown on these IPs' reputations via AbuseIPDB.")
    print("\nHeads Up: Make sure you look over and get to understand the script before running it.")
    print("=" * 60)
    
    user_input = input("Do you want to proceed? (yes/no): ")
    if user_input.lower() == 'yes':
        api_key = input("Input your www.abuseipdb.com API_KEY: ")
        print("This might take a while depending on the numbers of IP gathered from your PC so pleaseeeee be patient")
        check_network_connections()
        check_abuse_of_public_ips(api_key)
    else:
        print("No worries! Have an awesome day!")

    input("Press any key to exit...")