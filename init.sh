#!/bin/bash
INTERFACE="lo"

echo "Initializing netem rules..."
# we can also add reordering but it automatically happens since delay is random
sudo tc qdisc add dev "$INTERFACE" root netem delay 200ms 500ms distribution normal loss 30% corrupt 10%
echo "Netem rules applied."

read -rp "Press Enter to remove netem rules..."

echo "Removing netem rules..."
sudo tc qdisc del dev "$INTERFACE" root
echo "Netem rules removed."
