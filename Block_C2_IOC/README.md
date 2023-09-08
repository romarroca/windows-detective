# block-ip-win-defender.py

This script is designed to block connections that are either destined for or 
originating from Botnet C2 Indicators of Compromise (IOCs) from the past 30 days. 
You can verify the source data at "https://feodotracker.abuse.ch/blocklist/"

## How to use 
- Clone repo "git clone https://github.com/romarroca/windows-diy-antivirus"
- cd windows-diy-antivirus\Block_C2_IOC
- create python environment "python -m venv newenv"
- python block-ip-win-defender.py
- choose option "block"
![image](https://github.com/romarroca/windows-diy-antivirus/assets/87074019/da2b458c-5f3f-4ff7-98ce-aec5828f0b94)

## Important
Once the file is finished running, it will create new document with the list of IP that was added "blocked_ips.csv".
You will need this to automatically delete the added rules in case you do not want to add it anymore.
![image](https://github.com/romarroca/windows-diy-antivirus/assets/87074019/7d1c54ad-5e69-4e99-8311-6fb147321645)


## To remove
- just rerun the script and choose option "unblock"
![image](https://github.com/romarroca/windows-diy-antivirus/assets/87074019/055daf0b-3274-4c3f-a70e-fe51b59de619)


## Disclaimer: I use this script personally as an additional layer of security for my 
computer. While it aims to enhance security, it is not a guaranteed 
solution for protecting your PC. Use this script at your own risk and discretion. 
Make sure you understand its functionality before implementing it.
