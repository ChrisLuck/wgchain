import configparser
from pathlib import Path
from ipaddress import ip_address


MASK_SEP = "/"
PORT_SEP = ":"


def split_ip(ip_with_port: str, separator: str):
    ip, sep, port = ip_with_port.strip().rpartition(separator)
    assert sep # separator must be present
    ip = ip_address(ip.strip("[]")) # convert to `IPv4Address` or `IPv6Address` 
    return ip, int(port)


class IPWithMask():
    def __init__(self, ipwithmask):
        self.ip, self.mask = split_ip(ipwithmask, MASK_SEP)

    def __eq__(self, other):
        return self.ip == other.ip and self.mask == other.mask

    def __repr__(self):
        return str(self.ip) + MASK_SEP + str(self.mask)


class IPWithPort():
    def __init__(self, ipwithport: str):
        self.ip, self.port = split_ip(ipwithport, PORT_SEP)

    def __eq__(self, other):
        return self.ip == other.ip and self.port == other.port

    def __repr__(self):
        return str(self.ip) + PORT_SEP + str(self.port)


class IPList(list):
    def __repr__(self):
        return ", ".join(map(str, self))


class Interface():
    def __init__(self, **args):
        for (key, value) in args.items():
            match key.lower():
                case "address":
                    self.parse_address(value)
                case "listenport":
                    self.listenport = int(value)
                case "dns":
                    self.parse_dns(value)
                case "privatekey":
                    self.privatekey = value.strip()
                case "fwmark":
                    self.fwmark = value.strip()
                case _:
                    print("Unknown key in Interface: ", key)
                    exit(1)

    def parse_address(self, addr_val: str):
        self.address = IPList(IPWithMask(a) for a in addr_val.split(","))

    def parse_dns(self, dns_val: str):
        self.dns = IPList(ip_address(a.strip()) for a in dns_val.split(","))

    def __repr__(self):
        res = ""
        for key, value in self.__dict__.items():
            res += key + " = "
            res += str(value) + "\n"
        return res


class Peer():
    def __init__(self, **args):
        for (key, value) in args.items():
            match key.lower():
                case "allowedips":
                    self.parse_allowedips(value)
                case "publickey":
                    self.publickey = value.strip()
                case "endpoint":
                    self.parse_endpoint(value)
                case _:
                    print("Unknown key in Peer: ", key)
                    exit(2)

    def parse_allowedips(self, allowedips_val: str):
        self.allowedips = IPList(IPWithMask(a) for a in allowedips_val.split(","))

    def parse_endpoint(self, endpoint_val: str):
        self.endpoint = IPWithPort(endpoint_val)


class WgConfig():
    def __init__(self, cfg_file):
        self.cfgname = Path(cfg_file.name).name
        self.ifname = self.cfgname.removesuffix(".conf")

        cfg = configparser.ConfigParser()
        cfg.optionxform = str #otherwise keys are stored lowercase
        cfg.read_file(cfg_file)

        if 'Interface' in cfg:
            self.interface = Interface(**cfg['Interface'])

        if 'Peer' in cfg:
            self.peer = Peer(**cfg['Peer'])


    def write(self, file=Path('out.conf')):
        cfgparser = configparser.ConfigParser()
        cfgparser.optionxform = str #otherwise keys are stored lowercase

        cfgparser['Interface'] = self.interface.__dict__
        cfgparser['Peer'] = self.peer.__dict__

        with file.open('w') as configfile:
            cfgparser.write(configfile)
