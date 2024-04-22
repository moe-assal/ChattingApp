# Project
A chatting application that allows for peer-to-peer texting and file transfer. Technologies used are python sockets and PyQt5.

# Implementation
- We implemented a protocol on top of UDP that is based on RDT3.0 (used for texting)
- We implemented a file transfer protocol on top of TCP
- Simple GUI using PyQt5
- Timeout is estimated using statistical principles
- Configuration files in client.ini
- Aggressively tested using netem
- Documentation provided

# Run
- Client config files located in client.ini
- The two hosts should be able to directly communicate (Not behind NATs)
- Type `python -m main cleint.ini`
- You can run netem by typing `chmod +x init.sh` and `sudo ./init.sh`

# Documentation
Please check the report in the Documentation folder
