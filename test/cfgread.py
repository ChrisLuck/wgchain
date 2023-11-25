import unittest
from ipaddress import ip_address
from wgchain.wgconfig import IPList
from wgchain.wgconfig import Interface
from wgchain.wgconfig import Peer
from wgchain.wgconfig import IPWithMask
from wgchain.wgconfig import IPWithPort


class CfgReaderTestCase(unittest.TestCase):
    def testIPWithMask(self):
        ipwm = IPWithMask("10.0.0.2/24")
        self.assertEqual(ipwm.ip, ip_address("10.0.0.2"))
        self.assertEqual(ipwm.mask, 24)

        ipwm = IPWithMask("::/0")
        self.assertEqual(ipwm.ip, ip_address("::"))
        self.assertEqual(ipwm.mask, 0)

    def testIPWithPort(self):
        ipwp = IPWithPort("1.2.3.4:51820")
        self.assertEqual(ipwp.ip, ip_address("1.2.3.4"))
        self.assertEqual(ipwp.port, 51820)

    def testInterface(self):
        intf = Interface(Address="10.0.0.2/24",
                         ListenPort="51820 ",
                         PrivateKey=" myKey ")
        self.assertEqual(intf.address, [IPWithMask("10.0.0.2/24")])
        self.assertEqual(intf.address[0], IPWithMask("10.0.0.2/24"))
        self.assertEqual(intf.address[0].ip, ip_address("10.0.0.2"))
        self.assertEqual(intf.address[0].mask, 24)
        self.assertEqual(intf.listenport, 51820)
        self.assertEqual(intf.privatekey, "myKey")

    def testPeer(self):
        peer = Peer(allowedips="10.0.0.2/24, ::/0",
                    endpoint="1.2.3.4:51820")
        self.assertEqual(len(peer.allowedips), 2)
        self.assertEqual(peer.allowedips[0], IPWithMask("10.0.0.2/24"))
        self.assertEqual(peer.allowedips[0].ip, ip_address("10.0.0.2"))
        self.assertEqual(peer.allowedips[0].mask, 24)
        self.assertEqual(peer.allowedips[1], IPWithMask("::/0"))
        self.assertEqual(peer.endpoint, IPWithPort("1.2.3.4:51820"))
        self.assertEqual(peer.endpoint.ip, ip_address("1.2.3.4"))
        self.assertEqual(peer.endpoint.port, 51820)
