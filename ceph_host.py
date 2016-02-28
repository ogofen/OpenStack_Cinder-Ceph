from hosts import Host
from time import sleep

class CephHost(Host):
    def __init__(self, address, password):
        super(CephHost, self).__init__(address, password)
        
    def delete_pool(self, pool_name):
        cmd = "ceph osd pool delete %s %s --yes-i-really-really-mean-it" % (pool_name, pool_name)
        return self.run_bash_command(cmd)

    def create_pool(self, pool_name, pg_num):
        cmd = "ceph osd pool create %s %s" % (pool_name, pg_num)
        return self.run_bash_command(cmd)

    def create_and_allow_client(self, client_name, pool_name):

        cmd = "ceph auth get-or-create client.%s mon 'allow r' osd 'allow class-read " \
            "object_prefix rbd_children, allow rwx pool=%s'"  % (client_name, pool_name)
        client_conf_path = "/etc/ceph/ceph.client.%s.keyring" % client_name
        out = self.run_bash_command(cmd)
        return self.run_bash_command('echo "%s" > %s' % (out, client_conf_path))

    def delete_client(self, client_name):
        cmd = "ceph auth del client.%s" % client_name
        return self.run_bash_command(cmd)
        
