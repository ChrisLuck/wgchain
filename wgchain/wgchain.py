import argparse
from wgconfig import WgConfig
from wgconfig import IPList
from wgconfig import IPWithMask

COMMON_FWMARK = "51820"

parser = argparse.ArgumentParser(description='Build chain of VPNs.')

parser.add_argument('configs',
                    type=argparse.FileType('r'),
                    nargs='+',
                    help='wireguard configuration files')


args = parser.parse_args()

cfgs = list(map(WgConfig, args.configs))


#modify configs so that:
# - they all have the same FwMark
# - AllowedIPs of vpn #n is set to the endpoint of vpn #n+1
# - DNS?
before : WgConfig | None = None
for cfg in cfgs:
    cfg.interface.FwMark = COMMON_FWMARK
    if not before:
        before = cfg
        continue
    before.peer.AllowedIPs = IPList([IPWithMask(cfg.peer.Endpoint.ip + "/32")])

for cfg in cfgs:
    print("------")
    print(cfg.ifname)
    __import__('pprint').pprint(cfg.interface)
    __import__('pprint').pprint(cfg.peer)
    cfg.write(cfg.ifname + ".conf")
