"""Module containing logic for vlan and connection objects
"""
import random
import math
import logging
import ipaddress

gnd_logger = logging.getLogger("networkdata_generator")
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter(
        "[%(asctime)s::%(filename)s::%(funcName)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
)
gnd_logger.addHandler(console_handler)
gnd_logger.setLevel(logging.WARNING)


class NetworkHelper:
    """Helper class with static methods"""

    @staticmethod
    def get_src_port() -> int:
        """Returns a random source port

        Returns:
            int: Source port number between 49152 and 65535
        """
        # https://docs.microsoft.com/en-GB/troubleshoot/windows-server/networking/default-dynamic-port-range-tcpip-chang
        return random.randrange(49152, 65535)


class VlanIPv4Object:
    """vlan ipv4 object to hold vlan related logic"""

    def __init__(
        self,
        vlanname: str,
        networkmask: int = 24,
        innercoverage: int = 15,
        outercoverage: int = 25,
    ) -> None:
        """Initializes vlan ipv4 object and generates required data

        Args:
            vlanname (str): The desired vlan name
            networkmask (int, optional): Network mask to apply. Defaults to 24.
            innercoverage (int, optional): Percentage of hosts in the vlan connecting WITHIN the same vlan. Defaults to 15.
            outercoverage (int, optional): Percentage of hosts in the vlan connecting to OTHER vlans. Defaults to 25.
        """
        self.vlan_name = vlanname
        self.vlan_innercoverage = innercoverage
        self.vlan_outercoverage = outercoverage
        self.vlan_id = None
        self.vlan_ipv4range = None
        self._gen_vlanid()
        self._gen_vlanrange(networkmask)
        self.vlan_numhosts = len(list(self.vlan_ipv4range.hosts()))

    def _gen_vlanid(self, start: int = 1, end: int = 10000) -> None:
        """Generate a random vlan id

        Args:
            start (int, optional): Start of the range. Defaults to 1.
            end (int, optional): End of the range. Defaults to 10000.
        """
        self.vlan_id = random.randint(start, end)

    def _gen_vlanrange(self, mask: int) -> None:
        """Generate the ipv4 range for the vlan

        Args:
            mask (int): The desired network mask
        """
        octets = []
        for _ in range(4):
            octets.append(random.randint(0, 255))
        rndip = f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}/{mask}"
        gnd_logger.debug("rndip %s", rndip)
        self.vlan_ipv4range = ipaddress.IPv4Network(rndip, strict=False)

    def get_numhost_coverage(self, innercoverage: bool = True) -> int:
        """Get the amount of hosts available based on the coverage percentage

        Args:
            innercoverage (bool, optional): True if hosts are for WITHIN vlan use, False if hosts connect to OTHER vlans. Defaults to True.

        Returns:
            int: Amount of hosts available based on coverage percentage
        """
        if innercoverage:
            hostcount = math.floor(
                ((self.vlan_innercoverage / 100) * self.vlan_numhosts)
            )
        else:
            hostcount = math.floor(
                ((self.vlan_outercoverage / 100) * self.vlan_numhosts)
            )
        gnd_logger.debug("hostcount: %s", hostcount)
        return hostcount

    def get_rnd_ipv4host(self) -> ipaddress.IPv4Address:
        """Select a random host from all of the available hosts of the VLAN

        Returns:
            ipaddress.IPv4Address: The selected host
        """
        allhosts = list(self.vlan_ipv4range.hosts())
        rnd = random.randrange(1, self.vlan_numhosts)
        ipv4host = allhosts[rnd]
        gnd_logger.info("randomhost %s", ipv4host)
        return ipv4host

    def __repr__(self) -> str:
        """Override default repr function

        Returns:
            str: A dict representation of the class
        """
        return str(self.__dict__)

    def __str__(self) -> str:
        """Override default str function

        Returns:
            str: A dict representation of the class
        """
        return str(self.__dict__)


class VlanIPv4Connections:
    """vlan ipv4 connection object to hold all connection generating logic"""

    def __init__(
        self,
        srcvlan: VlanIPv4Object,
        dstvlan: VlanIPv4Object,
        dstports: list[tuple[int, str]],
        innerconnections: bool = True,
    ) -> None:
        """Instantiate connection object fields

        Args:
            srcvlan (VlanIPv4Object): The source vlan
            dstvlan (VlanIPv4Object): The destination vlan, can be the same if innerconnections is set to True
            dstports (list[tuple[int,str]]): The list of ports to use for outgoing connection. List consists of tuples (portnumber:int, servicename:str)
            innerconnections (bool, optional): Determines if connections are generated between hosts IN the vlan or from hosts in the vlan to OTHER vlans. Defaults to True.
        """
        self._srcvlan = srcvlan
        self._dstvlan = dstvlan
        self._dstports = dstports
        self._innerconnections = innerconnections

    def _get_host_pairs(self) -> list[tuple]:
        """Generates the source,destination host pairs

        Returns:
            list[tuple]: A list of tuples containing source and destination hosts
        """
        ipv4hosts = []
        totalhosts = 0
        if self._innerconnections:
            totalhosts = self._srcvlan.get_numhost_coverage()
        else:
            totalhosts = self._srcvlan.get_numhost_coverage(
                innercoverage=self._innerconnections
            )
        gnd_logger.debug("totalhosts %s", totalhosts)
        for _ in range(0, totalhosts):
            srchost = self._srcvlan.get_rnd_ipv4host()
            if self._innerconnections:
                dsthost = self._srcvlan.get_rnd_ipv4host()
            else:
                dsthost = self._dstvlan.get_rnd_ipv4host()
            gnd_logger.debug("srchost %s", srchost)
            gnd_logger.debug("dsthost %s", dsthost)
            while srchost == dsthost:
                dsthost = self._dstvlan.get_rnd_ipv4host()
                gnd_logger.debug("new dsthost %s", dsthost)
            gnd_logger.info("%s %s", srchost, dsthost)
            ipv4hosts.append((srchost, dsthost))
        return ipv4hosts

    def _get_dst_port(self) -> tuple[int, str]:
        """Get a random port from the list of destination ports

        Returns:
            tuple[int,str]: The randomly chosen destination tuple
        """
        maxport = len(self._dstports)
        rnd = random.randrange(0, maxport)
        return self._dstports[rnd]

    def get_host_connections(self) -> dict:
        """Generates the quadruple combination of source host, destination host, source port, destination port

        Returns:
            dict: A dict of connections containing srchost,dsthost,srcport,dstport
        """
        hosts = self._get_host_pairs()
        for pair in hosts:
            srcport = NetworkHelper.get_src_port()
            dstport = self._get_dst_port()[0]
            connection = {
                "srchost": str(pair[0]),
                "dsthost": str(pair[1]),
                "srcport": srcport,
                "dstport": dstport,
            }
            gnd_logger.info(
                "%s:%s %s:%s",
                connection["srchost"],
                connection["srcport"],
                connection["dsthost"],
                connection["dstport"],
            )
            yield (connection)
