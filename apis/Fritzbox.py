# Source: https://fritzconnection.readthedocs.io/en/1.3.4/sources/library.html#fritzwlan
# Note: Note: After Fritzbox OS update you often have to update Fritzconnection as well
# pip install fritzconnection==version

from fritzconnection.lib.fritzhosts import FritzHosts

class Fritzbox:
    def __init__(self, ipAddress, password): 
        # instanciate FritzWLAN just once for reusage
        self.__fh = FritzHosts(address=ipAddress, password=password)

    def getActiveMacs(self):
        active_macs = list()
        hosts = self.__fh.get_hosts_info()
        for index, host in enumerate(hosts, start=1):
            status = 'active' if host['status'] else  '-'
            ip = host['ip'] if host['ip'] else '-'
            mac = host['mac'] if host['mac'] else '-'
            hn = host['name']
            print(f'{index:>3}: {ip:<16} {hn:<28} {mac:<17}   {status}')
            if(status == 'active'):
                active_macs.append(host['mac'])

        return active_macs


    def getNumberActiveMacs(self, macs):
        activeMacs = self.getActiveMacs()
        numResidentsAtHome = 0
        # decide here what to do with this information:
        for mac in activeMacs:
            for macResident in macs:
                if mac == macResident:
                    numResidentsAtHome = numResidentsAtHome + 1

        # return number of macs = residents at home
        return numResidentsAtHome
