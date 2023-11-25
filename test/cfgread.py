import unittest
from wgchain.wgconfig import IPList
from wgchain.wgconfig import Interface
from wgchain.wgconfig import Peer
from wgchain.wgconfig import IPWithMask
from wgchain.wgconfig import IPWithPort

class CfgReaderTestCase(unittest.TestCase):
    def testIPWithMask(self):
        ipwm = IPWithMask("10.0.0.2/24")
        self.assertEqual(ipwm.ip, "10.0.0.2")
        self.assertEqual(ipwm.mask, 24)

        ipwm = IPWithMask("::/0")
        self.assertEqual(ipwm.ip, "::")
        self.assertEqual(ipwm.mask, 0)

    def testIPWithPort(self):
        ipwp = IPWithPort("vpn0.peer.endpoint.org:51820")
        self.assertEqual(ipwp.ip, "vpn0.peer.endpoint.org")
        self.assertEqual(ipwp.port, 51820)

    def testInterface(self):
        intf = Interface(Address="10.0.0.2/24",
                         ListenPort="51820 ",
                         PrivateKey=" myKey ")
        self.assertEqual(intf.Address, IPList([IPWithMask("10.0.0.2/24")]))
        self.assertEqual(intf.Address[0], IPWithMask("10.0.0.2/24"))
        self.assertEqual(intf.ListenPort, 51820)
        self.assertEqual(intf.PrivateKey, "myKey")

    def testPeer(self):
        peer = Peer("10.0.0.2/24, ::/0", "vpn0.peer.endpoint.org:51820")
        self.assertEqual(len(peer.AllowedIPs), 2)
        self.assertEqual(peer.AllowedIPs[0], IPWithMask("10.0.0.2/24"))
        self.assertEqual(peer.AllowedIPs[1], IPWithMask("::/0"))
        self.assertEqual(peer.Endpoint, IPWithPort("vpn0.peer.endpoint.org:51820"))
