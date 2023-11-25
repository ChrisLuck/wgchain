# wgchain
Create a chain of multiple WireGuard VPNs


### Usage:
    python3 wgchain/wgchain.py <chain_name> VPN0.conf VPN1.conf
    ./<chain_name>/activate.sh

### Result:
               you       VPN0      VPN1
    Inner VPN  O-------------------0
    Outer VPN  O=========0

    you -> VPN0 -> VPN1 -> internet

### Restrictions:
- only Linux
- only IPv4
- ???

### Why would someone want this?
When using one VPN it only needs this one VPN provider to be corrupt/hacked to link your internet activity to you.  
When using a chain of VPNs it needs _all_ VPN providers in that chain to be corrupt to link your internet activity to you.

This obviously only makes sense if you were careful when purchasing all VPNs in that chain:
- anonymous payment
- anonymous email
- anonymous connection used when purchasing
- anonymous connection used when downloading WireGuard configs
- ...

### How does it work?
- modify the given WireGuard configs in order to create this chain
- put iptables rules in place to ensure that data flow is only through this chain
