from openvpn_api import VPN
import math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])



class OpenVPN:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.vpn = None



    """"simply connect to the vpn instance"""
    def connect(self):
        try:
            self.vpn = VPN(self.ip,self.port)
            self.vpn.connect()
        except:
            print("failed to connect to vpn manager server")  
            return False
        
        return True


    def disconnect(self):
        try:
            self.vpn.disconnect()
        except:
            return False        
        return True




    def get_clients(self):
        try:
            connections = {}

            status = self.vpn.get_status()
            clients = status.client_list
            print(clients)
            
            
            for client,details in clients.items():
                print(details)
                connections[details.common_name] = {
                    "ip":client,
                    "bytes_received":convert_size(details.bytes_received),
                    "bytes_sent":convert_size(details.bytes_sent),
                }

        except Exception as e:
            print(f"{e}")
            return None
        return connections


