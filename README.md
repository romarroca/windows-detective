# network-detective.py
Runs a script that will perform netstat -anob and do reverse lookup, whois, and check abuse score from abuseipdb.com.
Running the script might take a while depending on the number of IP gathered from your PC.
After running the script, you will get 2 files:

- public_network_connections.txt : this is the list of public IP your windows PC is connecting to
- all_ip_reputations.json : This is the output from abuseipdb.com if you want to check on more of the details

# Before using
- It is suggested to run the script without any browser open to minimize noise.
- make sure to open command prompt in admin privilege as netstat -anob requires admin rights

# How to use (using the network-detective.py)
- Create free account from https://www.abuseipdb.com and get your api-key
      ![image](https://github.com/romarroca/windows-network-detective/assets/87074019/9bb25cdb-e81a-47cb-b110-cefe7703e42a)

- Setup python environment to not messed up your python libraries
      ![image](https://github.com/romarroca/windows-network-detective/assets/87074019/5528f8ad-6d05-4db6-9a38-9faa934e7204)

- clone the repository
    git clone https://github.com/romarroca/windows-network-detective
    ![image](https://github.com/romarroca/windows-network-detective/assets/87074019/881aca38-17ca-495a-b7c9-40d76a84221e)
- cd windows-network-detective ## change directory
- pip install -r requirements.txt ##This will install all requirements from requirements.txt
- Finally run the script script "python network-detective.py"
    ![image](https://github.com/romarroca/windows-network-detective/assets/87074019/ce8c21fe-eeaf-4e4b-8545-3cb5c79670db)

# How to use (using standalone .exe)
- Create free account from https://www.abuseipdb.com and get your api-key
      ![image](https://github.com/romarroca/windows-network-detective/assets/87074019/9bb25cdb-e81a-47cb-b110-cefe7703e42a)
  
- clone the repository
    git clone https://github.com/romarroca/windows-network-detective
    ![image](https://github.com/romarroca/windows-network-detective/assets/87074019/881aca38-17ca-495a-b7c9-40d76a84221e)

- cd windows-network-detective and navigate to "dist" folder ## change directory
- ![image](https://github.com/romarroca/windows-network-detective/assets/87074019/159c0dba-a347-42fc-9afa-ad36e6c4f01c)

- run the "network-detective.exe" as administrator
- ![image](https://github.com/romarroca/windows-network-detective/assets/87074019/4a0f36a4-78de-476a-af2f-dc1a3ac7b2e4)

- choose "yes" and enter your API key
        ![image](https://github.com/romarroca/windows-network-detective/assets/87074019/0f77b248-10eb-4991-95eb-960bfc6503dc)

## Disclaimer
Just a heads-up: this script dives into your network connections and pings some external servers to give you insights. Make sure you know what you're getting into before you run it, okay?

Run this script at your own risk. We've done our best to make it safe, but can't take the blame for any issues that pop up. Cool? Cool.

## Youtube video demo
- [Demo video](https://www.youtube.com/watch?v=LwYiy4V-JBU&t=480s)
