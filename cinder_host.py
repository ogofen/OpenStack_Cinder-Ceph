from hosts import Host
from time import sleep

class CinderHost(Host):
    def __init__(self, address, password):
        super(CinderHost, self).__init__(address, password)
        self.configure_ceph_str = "[ceph]\n"\
        "volume_driver = cinder.volume.drivers.rbd.RBDDriver\n"\
        "volume_backend_name = ceph\n"\
        "rbd_pool = %s\n"\
        "rbd_ceph_conf = /etc/ceph/ceph.conf\n"\
        "rbd_flatten_volume_from_snapshot = false\n"\
        "rbd_max_clone_depth = 5\n"\
        "rbd_store_chunk_size = 4\n"\
        "rados_connect_timeout = -1\n"\
        "rbd_user = %s\n"\
        "rbd_secret_uuid = a8152a42-73ba-4106-899a-226493b27bbf\n"

    def install_ceph_packages(self):
        self.install_package('ceph')
        seld.install_package('ceph-common')

    def add_ceph_to_cinder_conf(self, rbd_user, pool_name):
        conf_string = self.configure_ceph_str % (pool_name, rbd_user)
        cmd = 'echo "%s" >> /etc/cinder/cinder.conf' % (conf_string)
        return self.run_bash_command(cmd)

    def add_ceph_client_conf_files(self, rbd_user, pool_name):
        self.add_ceph_to_cinder_conf(rbd_user, pool_name)
        cmd = "ceph auth get-or-create client.%s mon 'allow r' osd 'allow class-read " \
            "object_prefix rbd_children, allow rwx pool=%s'"  % (rbd_user, pool_name)
        client_conf_path = "/etc/ceph/ceph.client.%s.keyring" % rbd_user
        out = self.run_bash_command(cmd)
        return self.run_bash_command("echo %s > %s" % (out, client_conf_path))


    def create_and_allow_client(self, client_name, pool_name):

        cmd = "ceph auth get-or-create client.%s mon 'allow r' osd 'allow class-read " \
            "object_prefix rbd_children, allow rwx pool=%s'"  % (client_name, pool_name)
        client_conf_path = "/etc/ceph/ceph.client.%s.keyring" % client_name
        out = self.run_bash_command(cmd)
        return self.run_bash_command("echo %s > %s" % (out, client_conf_path))

    def delete_client(self, client_name):
        cmd = "ceph auth del client.%s" % client_name
        return self.run_bash_command(cmd)
