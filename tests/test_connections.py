import pytest

from lib_networkdatagenerator.network.connections import NetworkHelper
from lib_networkdatagenerator.network.connections import VlanIPv4Object
from lib_networkdatagenerator.network.connections import VlanIPv4Connections

def test_get_src_port():
    portvalue = NetworkHelper.get_src_port()
    assert portvalue > 49152 and portvalue < 65535

class TestVlanIPv4Object:
    @pytest.mark.parametrize("input_coverage,expected", [(True,38), (False,63)])
    def test_get_numhost_coverage(self,input_coverage,expected):
        testvlan = VlanIPv4Object("testvlanname")
        numhosts = testvlan.get_numhost_coverage(innercoverage=input_coverage)
        assert numhosts == expected

class TestVlanIPv4Connections:
    @pytest.mark.parametrize("input_coverage,expected", [(True,38), (False,63)])
    def test_get_host_connections(self, input_coverage, expected):
        testvlan = VlanIPv4Object("testvlanname")
        testinsideconnections = VlanIPv4Connections(testvlan, testvlan, [(445,'smb')], innerconnections=input_coverage)
        genconn = sum(1 for _ in testinsideconnections.get_host_connections())
        assert expected == genconn