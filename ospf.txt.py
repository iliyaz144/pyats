from genie.testbed import load
from pprint import pprint
from genie.parsergen import oper_fill_tabular
from genie.utils import Dq
from genie.ops.utils import get_ops
import json
from collections import defaultdict
from collections import namedtuple

def get_ospf_neighState(index_value,field,index=0):
    tb=load('/home/dsalva/PycharmProjects/mse-cisco-R/mse-cisco/Resources/Source/InputFiles/testbed.yaml')
    dev = tb.devices['Automation-ASR9K-PE2']
    dev.connect()
    output = dev.device.execute('show ospf neighbor')
    header = ['Neighbor ID', 'Pri', 'State', 'Dead Time', 'Address', 'Interface']
    result = oper_fill_tabular(device_output=output, device_os='iosxr', header_fields=header,index=index)
    state=result.entries[index_value][field]
    dev.disconnect()
    return state


def get_ospf_neigh_state(neighIntf,neighAddr,instance='1',area='0.0.0.0'):
    tb=load('/home/dsalva/PycharmProjects/mse-cisco-R/mse-cisco/Resources/Source/InputFiles/testbed.yaml')
    dev = tb.devices['Automation-ASR9K-PE2']
    dev.connect()
    attributes = ['info[vrf][(.*)][address_family][ipv4]'
                  '[instance][(.*)]'
                  '[areas][(.*)]'
                  '[interfaces][(.*)]'
                  '[neighbors][(.*)]']
    ospf=dev.learn('ospf',attributes=attributes)
    neighState=ospf.info['vrf']['default']['address_family']['ipv4']['instance'][instance]['areas'][area]['interfaces'][neighIntf]['neighbors'][neighAddr].get('state')
    return neighState

def get_ospf_intf_state(self,dev,neighIntf,instance='1',area='0.0.0.0'):
    tb=load('/home/dsalva/PycharmProjects/mse-cisco-R/mse-cisco/Resources/Source/InputFiles/testbed.yaml')
    dev = tb.devices['Automation-ASR9K-PE2']
    dev.connect()
    attributes = ['info[vrf][(.*)][address_family][ipv4]'
                  '[instance][(.*)]'
                  '[areas][(.*)]'
                  '[interfaces][(.*)]']
    ospf=dev.learn('ospf',attributes=attributes)
    intfState=ospf.info['vrf']['default']['address_family']['ipv4']['instance'][instance]['areas'][area]['interfaces'][neighIntf].get('state')
    return intfState



#op=get_ospf_neighState('66.66.66.66','State')
#print(op)
#op=get_ospf_neigh_state('GigabitEthernet0/0/0/1','66.66.66.66')
#print("neighbor state:"+op)
#op=get_ospf_intf_state('GigabitEthernet0/0/0/1')
#print("intf state:"+op)