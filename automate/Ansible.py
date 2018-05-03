import os
import configparser
import subprocess
import shlex

"""
:class: Ansible
:input: playbook file name.
:function: handle a playbook object and execute it
:dependency in config file
    host_file: path of a list of host ip address that needs to be automatically manipulated
    user_name: ssh login name on target hosts
    key_file: path of .pem openssh key file of specific user when ssh login
"""


class Ansible:
    parser = configparser.ConfigParser(allow_no_value=True, delimiters=' ')

    def __init__(self, book_name):
        """
        Constructor of class ansible.
        :usage: book = Ansible.Ansible(path)
        :param
            book_name: String; the path of playbook file.
        """
        self.book = book_name

    def execute(self):
        """
        Set up ansible execution command, then execute the playbook.
        :usage: book.execute()
        :param: None
        :return: None
        """
        os.environ[""] = 'http://proxy_ip:port'
        subprocess.Popen('export', close_fds=True, shell=True, env=os.environ)
        command = "ansible-playbook"
        command += " -i" + self.parser["host_file"]
        command += " -u" + self.parser["user_name"]
        command += " --key-file" + self.parser["key_file"]
        command += " " + self.book
        process = subprocess.Popen(shlex.split(command))
        process.communicate()


if __name__ == "__main__":
    book = Ansible("deploy.yml")
    book.execute()

