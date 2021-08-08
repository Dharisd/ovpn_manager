from ovpn import OpenVpn

IP = "178.128.112.7"
PORT = 5555



s = OpenVpn(IP,PORT)

connect = s.connect()
print(connect)
clients = s.get_clients()

print(clients)
