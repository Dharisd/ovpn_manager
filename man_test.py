from ovpn_manager import OpenVPNManager


IP = "178.128.112.7"
PORT = 5555




c = OpenVPNManager(IP,PORT)
client_status = c.get_client_status()
config = c.gen_config("test_use6r")
p_status = c.get_ovpn_process_status()



print(client_status)
print(config)
print(p_status)

