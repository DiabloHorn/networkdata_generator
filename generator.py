#!/usr/bin/env python3
"""CLI interface to generate network data
"""
import argparse
import itertools

from network.connections import VlanIPv4Connections, VlanIPv4Object

#from config.jsonparser import ParseFile


def gen_vlan_connections(
    vlan_names: list[str], destination_ports: list[tuple[int, str]]
):
    """Generate the inner and outer VLAN connections

    Args:
        vlan_names (list[str]): The vlan names for which we generate the connection
        destination_ports (list[tuple[int,str]]): The set of destination ports that we want to use
    """
    for vln in vlan_names:
        vlan = VlanIPv4Object(vln)

        vlaninnerconnections = VlanIPv4Connections(vlan, vlan, destination_ports)
        for conn in vlaninnerconnections.get_host_connections():
            print(conn)

    print("====VLAN TO VLAN CONNECTIONS====")
    for bla in itertools.permutations(vlan_names, 2):
        srcvlan = VlanIPv4Object(vln[0])
        dstvlan = VlanIPv4Object(vln[1])

        vlaninnerconnections = VlanIPv4Connections(
            srcvlan, dstvlan, destination_ports, innerconnections=False
        )
        for conn in vlaninnerconnections.get_host_connections():
            print(conn)


if __name__ == "__main__":
    VLAN_NAMES = [
        "clients",
        "servers",
        "dmz",
        "databases",
        "voip",
        "admins",
        "servers_windows",
        "servers_linux",
    ]
    parser = argparse.ArgumentParser(
        description="Generate network connection with a varying level of metadata",
        epilog="Thanks for giving this a try! --DiabloHorn",
    )
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument(
        "--mode",
        choices=["inner", "outer", "all"],
        default="all",
        help="Generate only inner vlan, outer vlan or all connections",
    )
    subparsers = parser.add_subparsers(
        title="Available sub-commands",
        help="Generate connection dataset with different levels of metadata",
        dest="selectedsubparser",
    )

    parser_connections = subparsers.add_parser("plain", help="Only ip,src,ports")

    # maybe future functionality
    parser_timeconnections = subparsers.add_parser(
        "time", help="Adds timestamp within desired range"
    )
    parser_timeconnections.add_argument(
        "--timestart", default="20200101T01:00:00", help="ISO8601: YYYY-MM-DDTHH:MM:SS"
    )
    parser_timeconnections.add_argument(
        "--timestop", default="20200102T01:00:00", help="ISO8601: YYYY-MM-DDTHH:MM:SS"
    )

    # maybe future functionality
    parser_appconnections = subparsers.add_parser(
        "apps", help="Adds application details per connection"
    )
    parser_appconnections.add_argument("--exclude-apps")

    # maybe future functionality
    parser_full = subparsers.add_parser(
        "full", help="Generates connections with timestamps & application information"
    )

    args = parser.parse_args()
    
    configuration_file = None
    generation_mode = None

    if args.config:
        configuration_file = args.config
        #todo parse config
    if args.mode:
        generation_mode = args.mode

    if args.selectedsubparser:
        if args.selectedsubparser == 'plain':
            if generation_mode == 'inner':
                pass
            elif generation_mode == 'outer':
                pass
            elif generation_mode == 'all':
                pass
        elif args.selectedsubparser == 'time':
            print('Command not implemented')
        elif args.selectedsubparser == 'apps':
            print('Command not implemented')
        elif args.selectedsubparser == 'full':
            print('Command not implemented')
    

    
