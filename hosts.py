import paramiko
from time import sleep
import re


class Host(object):
    def __init__(self, address, psswd):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=address,
                             username='root',
                             password=psswd, timeout=15)
        except Exception, e:
            return e
        sleep(3)

    def __del__(self):
        self.ssh.close()

    def run_bash_command(self, bash_command):
        stdin, stdout, stderr = self.ssh.exec_command(bash_command)
        output = stdout.read()
        err = stderr.read()
        sleep(3)
        if output == '':
            return err
        return output

    def return_os(self):
        cmd = "cat /etc/redhat-release"
        str = self.run_bash_command(cmd)
        if "Fedora" in str:
            sleep(3)
            return "Fedora", re.findall(r'\d\.?\d', str)[0]
        else:
            sleep(3)
            return "Red Hat", re.findall(r'\d\.?\d', str)[0]

    def make_dir(self, path):
        cmd = "mkdir %s" % path
        try:
            self.run_bash_command(cmd)
        except Exception:
            return False
        sleep(3)
        return True

    def wget_file(self, dest, src):
        cmd = "wget -O %s %s --no-check-certificate" % (dest, src)
        try:
            self.run_bash_command(cmd)
        except Exception:
            return False
        sleep(3)
        return True

    def return_hostname(self):
        cmd = "dig -x %s" % (self.parameters['host_address'])
        try:
            str = self.run_bash_command(cmd)
        except Exception:
            return False
        sleep(3)
        return re.findall(r'R\t.+\.redhat\.com', str)[0][2:]

    def has_package(self, package):
        cmd = "rpm -qa | grep %s" % (package)
        if self.run_bash_command(cmd) is '':
            sleep(3)
            return False
        sleep(3)
        return True

    def set_hostname(self, hostname):
        cmd = "hostnamectl set-hostname %s" % (hostname)
        self.run_bash_command(cmd)
        sleep(3)

    def install_package(self, package):

        cmd = "yum install -y %s" % (package)
        self.run_bash_command(cmd)
        sleep(3)

    def has_file(self, path):
        ftp = self.ssh.open_sftp()
        try:
            ftp.lstat(path)
        except Exception:
            ftp.close()
            return False
        ftp.close()
        sleep(3)
        return True

    def delete_file(self, path):
        ftp = self.ssh.open_sftp()
        ftp.remove(path)
        ftp.close()
        sleep(3)

    def restart_services(self, service):
        cmd = "systemctl restart %s" % service
        self.run_bash_command(cmd)
        sleep(3)

    def put_file(self, localpath, remotepath):
        ftp = self.ssh.open_sftp()
        ftp.put(localpath, remotepath)
        sleep(5)
        ftp.close()
        sleep(3)
