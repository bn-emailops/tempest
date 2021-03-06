from tempest import openstack
from tempest.common.utils.data_utils import rand_name
from base_compute_test import BaseComputeTest
from tempest import exceptions
import tempest.config


class ServersNegativeTest(BaseComputeTest):

    @classmethod
    def setUpClass(cls):
        cls.client = cls.servers_client

    def test_server_name_blank(self):
        """Create a server with name parameter empty"""
        try:
            resp, server = self.client.create_server('', self.image_ref,
                                                     self.flavor_ref)
        except exceptions.BadRequest:
            pass
        else:
            self.fail('Server name cannot be blank')

    def test_personality_file_contents_not_encoded(self):
        """Use an unencoded file when creating a server with personality"""
        file_contents = 'This is a test file.'
        personality = [{'path': '/etc/testfile.txt',
                        'contents': file_contents}]

        try:
            resp, server = self.client.create_server('test',
                                                      self.image_ref,
                                                      self.flavor_ref,
                                                      personality=personality)
        except exceptions.BadRequest:
            pass
        else:
            self.fail('Unencoded file contents should not be accepted')

    def test_create_with_invalid_image(self):
        """Create a server with an unknown image"""
        try:
            resp, server = self.client.create_server('fail', -1,
                                                     self.flavor_ref)
        except exceptions.BadRequest:
            pass
        else:
            self.fail('Cannot create a server with an invalid image')

    def test_create_with_invalid_flavor(self):
        """Create a server with an unknown flavor"""
        try:
            self.client.create_server('fail', self.image_ref, -1)
        except exceptions.BadRequest:
            pass
        else:
            self.fail('Cannot create a server with an invalid flavor')

    def test_invalid_access_ip_v4_address(self):
        """An access IPv4 address must match a valid address pattern"""
        accessIPv4 = '1.1.1.1.1.1'
        name = rand_name('server')
        try:
            resp, server = self.client.create_server(name,
                                                     self.image_ref,
                                                     self.flavor_ref,
                                                     accessIPv4=accessIPv4)
        except exceptions.BadRequest:
            pass
        else:
            self.fail('Access IPv4 address must match the correct format')

    def test_invalid_ip_v6_address(self):
        """An access IPv6 address must match a valid address pattern"""
        accessIPv6 = 'notvalid'
        name = rand_name('server')
        try:
            resp, server = self.client.create_server(name,
                                                     self.image_ref,
                                                     self.flavor_ref,
                                                     accessIPv6=accessIPv6)
        except exceptions.BadRequest:
            pass
        else:
            self.fail('Access IPv6 address must match the correct format')

    def test_reboot_deleted_server(self):
        """Reboot a deleted server"""
        self.name = rand_name('server')
        resp, create_server = self.client.create_server(self.name,
                                                 self.image_ref,
                                                 self.flavor_ref)
        self.server_id = create_server['id']
        self.client.delete_server(self.server_id)
        try:
            resp1, reboot_server = self.client.reboot(self.server_id, 'SOFT')
        except exceptions.NotFound:
            pass
        else:
            self.fail('Should not be able to reboot a deleted server')

    def test_rebuild_deleted_server(self):
        """Rebuild a deleted server"""
        self.name = rand_name('server')
        resp, create_server = self.client.create_server(self.name,
                                                 self.image_ref,
                                                 self.flavor_ref)
        self.server_id = create_server['id']
        self.client.delete_server(self.server_id)
        try:
            resp1, rebuild_server = self.client.rebuild(self.server_id,
                                                self.image_ref_alt)
        except exceptions.NotFound:
            pass
        else:
            self.fail('Should not be able to rebuild a deleted server')
