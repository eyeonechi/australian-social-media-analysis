"""
@Team info:
    CCC Team 42 (Melbourne)
    Hannah Ha   963370
    Lan Zhou    824371
    Zijian Wang 950618
    Ivan Chee   736901
    Duer Wang   824325
@Module: Ansible
@input: playbook file name.
@function: handle a playbook object and execute it
@dependency in config file
   host_file: path of a list of host ip address that needs to be automatically manipulated
   user_name: ssh login name on target hosts
   key_file: path of .pem openssh key file of specific user when ssh login
"""
import configparser
import subprocess
import shlex


class Ansible:

    def __init__(self, book_name):
        """
        Constructor of class ansible.
        :usage: book = Ansible.Ansible(path)
        :param
            book_name: String; the path of playbook file.
        """
        self.parser = configparser.ConfigParser()
        self.parser.read(r'config.ini')
        self.book = book_name

    def execute(self):
        """
        Set up ansible execution command, then execute the playbook.
        :usage: book.execute()
        :param: None
        :return: None
        """
        command = "ansible-playbook"
        command += " -i " + self.parser["host_file"]["name"]
        command += " -u " + self.parser["user_name"]["name"]
        command += " --key-file " + self.parser["key_file"]["name"]
        command += " " + self.book
        process = subprocess.Popen(shlex.split(command))
        process.communicate()


if __name__ == "__main__":
    book = Ansible("deploy.yml")
    book.execute()

