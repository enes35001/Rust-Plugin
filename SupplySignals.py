__author__ = 'Assassin'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

#Start Of Config Is Here
BlockSupplySignals=0
SupplyMessage=1

#End Of Config


class SupplySignals:

    def On_SupplySignalExploded(self, SupplySignalExplosionEvent):
        if BlockSupplySignals == 1:
            Server.Broadcast("[color red]Supply Signals Won't Work In This Server!!")
            SupplySignalExplosionEvent.Cancel()
        else:
            if SupplyMessage == 1:
                Server.Broadcast(" Someone Throwed a Supply Signal!Try To Find Him")
				Server.Broadcast(" Biri Hava Yardımı istedi ! Git ve Onu Bul")