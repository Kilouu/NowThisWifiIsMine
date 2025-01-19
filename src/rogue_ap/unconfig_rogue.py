
'''
sudo iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -D FORWARD -i wlan0 -j ACCEPT
sudo iptables -t nat -D PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.1

sudo iptables -t nat -L POSTROUTING --line-numbers
sudo iptables -L FORWARD --line-numbers
sudo iptables -t nat -L PREROUTING --line-numbers
'''

