#!/usr/bin/env python3
"""CLI interface to generate network data
"""
import itertools


from network.connections import vlan_ipv4_object
from network.connections import vlan_ipv4_connections


if __name__ == "__main__":
    #configtemplate = [{'vlanname':'clients','innercoverage':15,'outercoverage':25,'innerports':[((445,'smb'),(3389,'rdp'))],'outerports':[(80,'http'),(389,'ldap')]}]
    VLAN_NAMES = ['clients','servers','dmz','databases','voip','admins','servers_windows','servers_linux']

    for vln in VLAN_NAMES:
        vlan = vlan_ipv4_object(vln)

        vlaninnerconnections = vlan_ipv4_connections(vlan,vlan,[(445,'smb'),(3389,'rdp')])
        for conn in vlaninnerconnections.get_host_connections():
            print(conn)

    print("====VLAN TO VLAN CONNECTIONS====")
    for bla in itertools.permutations(VLAN_NAMES, 2):
        srcvlan = vlan_ipv4_object(vln[0])
        dstvlan = vlan_ipv4_object(vln[1])

        vlaninnerconnections = vlan_ipv4_connections(srcvlan,dstvlan,[(445,'smb'),(3389,'rdp')],innerconnections=False)
        for conn in vlaninnerconnections.get_host_connections():
            print(conn)
