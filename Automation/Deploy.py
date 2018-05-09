import Ansible
import Nectar
import time
import configparser
import socket
import sys


class Deploy:

    def __init__(self, type):
        self.parser = configparser.ConfigParser()
        self.parser.read(r'config.ini')
        self.type = type
        self.nectar = Nectar.Nectar()

    def set_machine(self):
        machine = self.nectar.add_instance()
        return machine

    def deploy_application(self, script_name):
        """
        Execute automation script to deploy the application.
        :param: script_name: string, the type of machine
        :return: None
        """
        ansible_get_repo = Ansible.Ansible("./scripts/" + script_name + ".yml")
        ansible_get_repo.execute()

    def main(self):
        # ------------------------------------------------------------
        # Set up the virtual machine, create a volume and attach it.
        print("Start establishing virtual machine..")
        vm_info = deploy.set_machine()
        vm_id = vm_info["id"]
        vm_state = vm_info["state"]
        while vm_state != "running":
            time.sleep(3)
            vm_state = self.nectar.get_instance_info(vm_id)["state"]
            print("Instance status: " + vm_state)
        self.nectar.add_volume(vm_id)
        print("Instance " + self.nectar.get_instance_info(vm_id)["ip"] + " successfully established.")

        vm_ip = self.nectar.get_instance_info(vm_id)["ip"]
        self.write_config(self.type, vm_ip)
        self.write_machine_config(vm_ip)
        print("Testing ssh port of target server...")
        while not self.check_port(vm_ip, 22):
            time.sleep(3)

        # ------------------------------------------------------------
        # Execute ansible script to configure the machine and install software.
        print("Start installing dependencies and softwares on the machine.")
        self.deploy_application("set_volume")
        self.deploy_application("deploy_app")
        if self.type == "database":
            self.deploy_application("webservice")
            self.deploy_application("database")
        elif self.type == "harvester":
            self.deploy_application("harvester")
        elif self.type == "analyser":
            self.deploy_application("spark")
        else:
            print("ERROR: Incorrect machine type.")
        
        #-------------------------------------------------------------
        # Configure and start service.
        print("Software installing compliete. Start running application.")

    def write_config(self, key, value):
        cfgfile = open("config.ini", 'w')
        self.parser.set("options", key, value)
        self.parser.write(cfgfile)
        cfgfile.close()

    def write_machine_config(self, ip):
        lines = []
        f = open("ansible_hosts.ini", "r", encoding='utf-8')
        line = f.readline()
        while line:
            lines.append(line)
            if self.type in line:
                lines.append(ip)
            line = f.readline()
        f.close()
        s = "\n".join(lines)
        f = open("ansible_hosts.ini", "w", encoding="utf-8")
        f.write(s)
        f.close()

    def check_port(self, address, port):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect((address,port))
            print("Server ssh port OK.")
            return True
        except:
            return False


if __name__ == "__main__":
    deploy = Deploy(sys.argv[1])
    deploy.main()


