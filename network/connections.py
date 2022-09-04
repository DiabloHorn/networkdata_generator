import random
import math
import logging
import ipaddress

gnd_logger = logging.getLogger('networkdata_generator')
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('[%(asctime)s::%(filename)s::%(funcName)s] %(message)s',"%Y-%m-%d %H:%M:%S"))
gnd_logger.addHandler(console_handler)
gnd_logger.setLevel(logging.WARNING)

class network_helper:
    def __init__(self):
        pass

    @staticmethod
    def get_src_port():
        # https://docs.microsoft.com/en-GB/troubleshoot/windows-server/networking/default-dynamic-port-range-tcpip-chang
        return random.randrange(49152,65535)

class vlan_ipv4_object:
    def __init__(self,vlanname,networkmask=24,innercoverage=15,outercoverage=25):
        self.vlan_name = vlanname
        self.vlan_innercoverage = innercoverage
        self.vlan_outercoverage = outercoverage
        self.vlan_id = None
        self.vlan_ipv4range = None
        self._gen_vlanid()
        self._gen_vlanrange(networkmask)
        self.vlan_numhosts = len(list(self.vlan_ipv4range.hosts()))

    def _gen_vlanid(self,start=1,end=10000):
        self.vlan_id = random.randint(start,end)

    def _gen_vlanrange(self,mask):
        octets = []
        for _ in range(4):
            octets.append(random.randint(0,255))
        rndip = f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}/{mask}"
        gnd_logger.debug("rndip %s", rndip)
        self.vlan_ipv4range = ipaddress.IPv4Network(rndip,strict=False)

    def get_numhost_coverage(self, innercoverage=True):
        if innercoverage:
            hostcount = math.floor(((self.vlan_innercoverage/100)*self.vlan_numhosts))
        else:
            hostcount = math.floor(((self.vlan_outercoverage/100)*self.vlan_numhosts))
        gnd_logger.debug("hostcount: %s", hostcount)
        return hostcount

    def get_rnd_ipv4host(self):
        allhosts = list(self.vlan_ipv4range.hosts())
        rnd = random.randrange(1,self.vlan_numhosts)
        ipv4host = allhosts[rnd]
        gnd_logger.info("randomhost %s", ipv4host)
        return ipv4host

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

class vlan_ipv4_connections:
    def __init__(self,srcvlan:vlan_ipv4_object,dstvlan:vlan_ipv4_object,dstports,innerconnections=True):
        self._srcvlan = srcvlan
        self._dstvlan = dstvlan
        self._dstports = dstports
        self._innerconnections = innerconnections

    def _get_host_pairs(self):
        ipv4hosts = []
        totalhosts = 0
        if self._innerconnections:
            totalhosts = self._srcvlan.get_numhost_coverage()
        else:
            totalhosts = self._srcvlan.get_numhost_coverage(innercoverage=self._innerconnections)
        gnd_logger.debug("totalhosts %s", totalhosts)
        for _ in range(0,totalhosts):
            srchost = self._srcvlan.get_rnd_ipv4host()
            if self._innerconnections:
                dsthost = self._srcvlan.get_rnd_ipv4host()
            else:
                dsthost = self._dstvlan.get_rnd_ipv4host()
            gnd_logger.debug("srchost %s", srchost)
            gnd_logger.debug("dsthost %s", dsthost)
            while(srchost == dsthost):
                dsthost = self._dstvlan.get_rnd_ipv4host()
                gnd_logger.debug("new dsthost %s", dsthost)
            gnd_logger.info("%s %s",srchost,dsthost)
            ipv4hosts.append((srchost,dsthost))
        return ipv4hosts
   
    def _get_dst_port(self):
        maxport = len(self._dstports)
        rnd = random.randrange(0,maxport)
        return self._dstports[rnd]

    def get_host_connections(self):
        hosts = self._get_host_pairs()
        for pair in hosts:
            srcport = network_helper.get_src_port()
            dstport = self._get_dst_port()[0]
            connection = {"srchost":str(pair[0]),"dsthost":str(pair[1]),"srcport":srcport,"dstport":dstport}
            gnd_logger.info("%s:%s %s:%s", connection['srchost'],connection['srcport'],connection['dsthost'],connection['dstport'])
            yield(connection)
