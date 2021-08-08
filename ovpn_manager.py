from ovpn import OpenVPN
import os
import subprocess


""""ideally would support mulitple servers"""
class OpenVPNManager():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port


    def get_client_status(self):
        try:
            conn = OpenVPN(self.ip,self.port)
            conn.connect()
            clients = conn.get_clients()
            conn.disconnect()
        except Exception as e:
            print(f"error in fetching status {f}")
            return False
        
        return clients

    def gen_config(self,client_name):
        path = ""
        try:
            path = "/etc/openvpn/client/"
            config_file = os.system(f"./gen_client.sh {client_name}")
            path = path+f"{client_name}.ovpn"
        except Exception as e:
            print(f"{e}")
            print("config already exists")
        
        return f"{path}" 

    def get_ovpn_process_status(self):
        status = os.system('systemctl  is-active openvpn@server.service')
        if status == 0:
            return "active"
        
        return "dead"
    
    def get_squid_process_status(self):
        status = os.system('systemctl is-active  squid')
        if status == 0:
            return "active"
        
        return "dead"


    def restart_squid(slef):
        subprocess.run("systemctl restart squid")

        return True

    def restart_ovpn():
        subprocess.run("systemctl restart openvpn@server.service")
        return True





        






    






