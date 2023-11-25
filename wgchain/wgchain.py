import argparse
import subprocess
from string import Template
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
# - They all have the same FwMark
# - AllowedIPs of vpn #n is set to the endpoint of vpn #n+1
# - DNS addresses af all configs removed except from last/innermost one
before: WgConfig | None = None
for cfg in cfgs:
    cfg.interface.fwmark = COMMON_FWMARK
    if not before:
        before = cfg
        continue
    before.peer.allowedips = IPList([IPWithMask(str(cfg.peer.endpoint.ip) + "/32")])

    # remove DNS from every config except last/innermost one
    del before.interface.dns


# Sanity checks for DNS fields
for cfg in cfgs[:-1]:
    assert not hasattr(cfg.interface, "dns"), "Code for DNS removal is faulty"
assert hasattr(cfgs[-1].interface, "dns"), "Risk of leakage: Innermost config has no DNS field."


for cfg in cfgs:
    print("------")
    print(cfg.ifname)
    __import__('pprint').pprint(cfg.interface)
    __import__('pprint').pprint(cfg.peer)
    cfg.write(cfg.ifname + ".conf")


if len(cfgs) == 2:
    ifacename = subprocess.check_output("ip -o -f inet addr show | awk '/scope global/ {print $2}'", shell=True)
    ifacename = ifacename.decode().strip()
    localnet  = subprocess.check_output("ip -o -f inet addr show | awk '/scope global/ {print $4}'", shell=True)
    localnet  = localnet.decode().strip()


    template = None
    with open("wgchain/fwtemplate.sh", "r") as f:
        template = Template(f.read())

    with open("fwon.sh", "w") as outfile:
        mapping = {"IFACENAME":ifacename,
                   "LOCALNET":localnet,
                   "VPN0":cfgs[0].ifname,
                   "VPN1":cfgs[1].ifname,
                   "VPN0_EP_IP":cfgs[0].peer.endpoint.ip,
                   "VPN0_EP_PORT":cfgs[0].peer.endpoint.port,
                   "VPN1_EP_IP":cfgs[1].peer.endpoint.ip,
                   "VPN1_EP_PORT":cfgs[1].peer.endpoint.port}
        outfile.write(template.substitute(mapping))
