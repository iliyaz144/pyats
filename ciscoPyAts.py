import sys
import re
import time
from MyLog import MyLog
from genie.testbed import load
LOG= MyLog('junosPyEz.py','DEBUG')
import os


class ciscoPyAts(object):
    def __init__(self):
        print('Object instantial')
        
    def connect_to_device(self,inputFile,device): 
        dirPath= os.path.dirname(os.path.abspath(__file__))
        dstFolder= os.path.dirname(os.path.abspath(dirPath))
        filepath=dstFolder+"/InputFiles/"+inputFile
        tb = load(filepath)
        try:
            dev = tb.devices[device]
            dev.connect()
        except:
            LOG.info ("Cannot connect to device: {0}".format(err))
            sys.exit(1)
        return dev 
    
    def disconnect_device(self,dev):
        dev.disconnect()

    def run_show_command(self,dev,command):
        response = dev.execute(command)
        print(response)
        return response
    
    def show_interfaces_statistics(self,dev,interfaceName,field):
        '''
        some fields can retrieve are 'oper_status','counters': {'rate': {'load_interval': 30, 'in_rate': 0, 'in_rate_pkts': 0, 'out_rate': 0, 'out_rate_pkts': 0}'
        '''
        stats=list()
        response=dev.parse('show interface %s detail'%interfaceName)
        for item in field:
            status= response[interfaceName][item]
            stats.append(status)
        return stats   
  
    def ping_host_address(self,dev,destAddr):  
        '''
        Ping from cisco router with given address and return the packet loss
        '''
        try:
            cli_output=dev.execute('ping %s'%destAddr)
            desireLine=re.findall("Success rate .+$",cli_output,re.MULTILINE)
            sucRate=re.match(r'Success rate is (\d+) percent .*$',desireLine[0])
            successRate=sucRate.group(1)
        except IndexError as error:
            return error
        return  successRate
    
    def check_bgp_neigbor_status(self,dev,neighbor):
        response=dev.parse('show bgp neighbors %s'%neighbor)
        state=(response['instance']['all']['vrf']['default']['neighbor'][neighbor]['session_state'])
        return state

    def get_ospf_neigh_state(self,dev,neighIntf,neighAddr,instance='1',area='0.0.0.0'):
        attributes = ['info[vrf][(.*)][address_family][ipv4]'
                  '[instance][(.*)]'
                  '[areas][(.*)]'
                  '[interfaces][(.*)]'
                  '[neighbors][(.*)]']
        ospf=dev.learn('ospf',attributes=attributes)
        neighState=ospf.info['vrf']['default']['address_family']['ipv4']['instance'][instance]['areas'][area]['interfaces'][neighIntf]['neighbors'][neighAddr].get('state')
        return neighState

    def get_ospf_intf_state(self,dev,neighIntf,instance='1',area='0.0.0.0'):
        attributes = ['info[vrf][(.*)][address_family][ipv4]'
                  '[instance][(.*)]'
                  '[areas][(.*)]'
                  '[interfaces][(.*)]']
        ospf=dev.learn('ospf',attributes=attributes)
        intfState=ospf.info['vrf']['default']['address_family']['ipv4']['instance'][instance]['areas'][area]['interfaces'][neighIntf].get('state')
        return intfState

    def config_device(self,dev,command):
            dev.configure(command)
        
    
            