#!/bin/bash
#
#            me       VPN0      VPN1
# Inner VPN  O-------------------0
# Outer VPN  O=========0
#
# me -> $VPN0 -> $VPN1 -> internet

set -e
set -o pipefail


wg-quick up ./$VPN0.conf
wg-quick up ./$VPN1.conf


#disable ipv6
sysctl -w net.ipv6.conf.all.disable_ipv6=1
sysctl -w net.ipv6.conf.default.disable_ipv6=1
sysctl -w net.ipv6.conf.lo.disable_ipv6=1

#allow local network communication outside of tunnel
iptables -A OUTPUT -o $IFACENAME -d $LOCALNET -j ACCEPT

iptables -A OUTPUT -o $IFACENAME -p udp ! --dport $VPN0_EP_PORT -j REJECT
iptables -A OUTPUT -o $IFACENAME ! -d $VPN0_EP_IP -j REJECT

iptables -A OUTPUT -o $VPN0 -p udp ! --dport $VPN1_EP_PORT -j REJECT
iptables -A OUTPUT -o $VPN0 ! -d $VPN1_EP_IP -j REJECT
