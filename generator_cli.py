#!/usr/bin/env python3
"""CLI interface to generate network data
"""
import argparse
import itertools
import logging

from lib_networkdatagenerator.base_logger.mylogger import gnd_logger
from lib_networkdatagenerator.config.jsonparser import ParseConfigFile
from lib_networkdatagenerator.network.connections import (VlanIPv4Connections,
                                                          VlanIPv4Object)


def gen_plain_inner(vlan_objects: list[dict]):
    """Generate all inner VLAN connections

    Args:
        vlan_objects (list[dict]): A VLAN configuration object
    """
    for vln in vlan_objects:
        vlan = VlanIPv4Object(vln["vlanname"])
        vlaninnerconnections = VlanIPv4Connections(vlan, vlan, vln["tcpinnerports"])
        for conn in vlaninnerconnections.get_host_connections():
            print(conn)


def gen_plain_outer(vlan_objects: list[dict]):
    """Generate all outer VLAN connections

    Args:
        vlan_objects (list[dict]): A VLAN configuration object
    """
    for vlanobject in itertools.permutations(vlan_objects, 2):
        if not vlanobject[0]["tcpouterports"]:
            continue
        srcvlan = VlanIPv4Object(vlanobject[0]["vlanname"])
        dstvlan = VlanIPv4Object(vlanobject[1]["vlanname"])

        vlaninnerconnections = VlanIPv4Connections(
            srcvlan, dstvlan, vlanobject[0]["tcpouterports"], innerconnections=False
        )
        for conn in vlaninnerconnections.get_host_connections():
            print(conn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate network connection with a varying level of metadata",
        epilog="Thanks for giving this a try! --DiabloHorn",
    )

    parser.add_argument(
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        help="set debug level",
    )
    parser.add_argument(
        "--verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        help="set informational level",
    )
    parser.add_argument("--config", default="config.json", help="Configuration file")
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
    if args.loglevel:
        gnd_logger.setLevel(args.loglevel)
    configparser = ParseConfigFile(args.config)

    if args.selectedsubparser:
        if args.selectedsubparser == "plain":
            if args.mode == "inner":
                gen_plain_inner(configparser.get_inner_vlans())
            elif args.mode == "outer":
                gen_plain_outer(configparser.get_all_vlans())
            elif args.mode == "all":
                gen_plain_inner(configparser.get_inner_vlans())
                gen_plain_outer(configparser.get_all_vlans())
        elif args.selectedsubparser == "time":
            print("Command not implemented")
        elif args.selectedsubparser == "apps":
            print("Command not implemented")
        elif args.selectedsubparser == "full":
            print("Command not implemented")
