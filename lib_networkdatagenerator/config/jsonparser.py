"""Parse JSON config
"""

import json

from lib_networkdatagenerator.base_logger.mylogger import gnd_logger


class ParseConfigFile:
    """Parse a JSON file config"""

    def __init__(self, configpath: str) -> None:
        """Loads the JSON config into python structures

        Args:
            configpath (str): File location of the json configuration file
        """        
        self.configlocation:str = configpath
        self.config_raw:list[dict] = list()
        self._loadjson()
        gnd_logger.debug("Initialized")

    def _loadjson(self) -> None:
        """Wrapper for json.load()
        """
        with open(self.configlocation, encoding="utf-8") as configfile:
            self.config_raw = json.load(configfile)
            gnd_logger.debug("loaded json config %s", self.config_raw)

    def get_all_vlans(self) -> list[dict]:
        """Returns a list of all VLANs

        Returns:
            list[dict]: List containing per VLAN configuration
        """
        return self.config_raw

    def get_inner_vlans(self) -> list[dict]:
        """Returns all VLANs with non-empty tcpinnerports

        Returns:
            list[dict]: List containing per VLAN configuration
        """
        gnd_logger.debug("original inner vlans: %s", self.config_raw)
        filtered = filter(lambda v: len(v['tcpinnerports']) != 0, self.config_raw)
        return list(filtered)
