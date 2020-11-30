# Source: https://fritzconnection.readthedocs.io/en/1.3.4/sources/library.html#fritzwlan

import itertools

from fritzconnection.lib.fritzwlan import FritzWLAN
from fritzconnection.core.exceptions import FritzServiceError

class Fritzbox:
    def __init__(self, ipAddress, password): 
        # instanciate FritzWLAN just once for reusage
        self.__fwlan = FritzWLAN(address=ipAddress, password=password)

    def getActiveMacs(self):
        """
        Gets a FritzWLAN instance and returns a list of mac addresses
        from the active devices
        """
        active_macs = list()
        # iterate over all wlans:
        for n in itertools.count(1):
            self.__fwlan.service = n
            try:
                hostsInfo = self.__fwlan.get_hosts_info()
            except FritzServiceError:
                break
            else:
                active_macs.extend(entry['mac'] for entry in hostsInfo)
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
