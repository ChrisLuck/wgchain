import configparser
from pathlib import Path
from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar

IP_MASK_DELIM = "/"
IP_PORT_DELIM = ":"


class IPList(list):
    def __repr__(self):
        return ", ".join(map(str, self))


@dataclass
class IPWithPort:
    raw:  InitVar[str]
    ip:   str = field(init=False)
    port: int = field(init=False)

    def __post_init__(self, raw):
        raw  = raw.strip()
        self.ip   = raw.split(IP_PORT_DELIM)[0]
        self.port = int(raw.split(IP_PORT_DELIM)[1])

    def __repr__(self):
        return self.ip + IP_PORT_DELIM + str(self.port)


@dataclass
class IPWithMask:
    raw:  InitVar[str]
    ip:   str = field(init=False)
    mask: int = field(init=False)

    def __post_init__(self, raw):
        raw  = raw.strip()
        self.ip   = raw.split(IP_MASK_DELIM)[0]
        self.mask = int(raw.split(IP_MASK_DELIM)[1])

    def __repr__(self):
        return self.ip + IP_MASK_DELIM + str(self.mask)


@dataclass
class Interface:
    PrivateKey:  str
    Address:     IPList | str
    ListenPort:  int | str | None    = field(default=None)
    FwMark:      str | None          = field(default=None)
    DNS:         IPList | str | None = field(default=None)

    def __post_init__(self):
        self.PrivateKey = self.PrivateKey.strip()
        if type(self.Address) == str:
            self.Address = IPList(map(lambda x: IPWithMask(x.strip()),
                                      self.Address.split(",")))
        if type(self.ListenPort) == str:
            self.ListenPort = int(self.ListenPort)
        if type(self.FwMark) == str:
            self.FwMark = self.FwMark.strip()
        if type(self.DNS) == str:
            self.DNS = IPList(map(lambda x: x.strip(),
                              self.DNS.split(",")))


@dataclass
class Peer:
    AllowedIPs: IPList | str
    Endpoint:   IPWithPort | str
    PublicKey:  str = field(default="")

    def __post_init__(self):
        if type(self.AllowedIPs) == str:
            self.AllowedIPs = IPList(map(lambda x: IPWithMask(x.strip()),
                              self.AllowedIPs.split(",")))
        if type(self.Endpoint) == str:
            self.Endpoint = IPWithPort(self.Endpoint)
        self.PublicKey = self.PublicKey.strip()


# dataclass does not allow optional fields so I am working around this by
# setting fields to None and filtering them later with this function.
def filter_dict(inputdict: dict) -> dict:
    return dict((k, v) for k, v in inputdict.items() if v != None )


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

    def write(self, file='out.conf'):
        cfgparser = configparser.ConfigParser()
        cfgparser.optionxform = str #otherwise keys are stored lowercase

        cfgparser['Interface'] = filter_dict(self.interface.__dict__)
        cfgparser['Peer'] = filter_dict(self.peer.__dict__)

        with open(file, 'w') as configfile:
            cfgparser.write(configfile)
