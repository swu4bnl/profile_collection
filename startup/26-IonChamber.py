# from nslsii.ad33 import QuadEMV33
# # from ophyd import Signal
# # from ophyd import Component as Cpt
# #from ophyd.quadem import TetrAMM

# class new_qm(QuadEMV33):
#     corrected_signal = Cpt(Signal,name='corrected_signal',value=0.0,kind='hinted')
    
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args, **kwargs)
#         self.current2.mean_value.subscribe(self.update_monitor)
        
#     def update_monitor(self,old_value,value,**kwargs):

#         atten_2 = int(S3.absorber1.user_readback.value)
#         attenuator_name_signal.set(f'att{atten_2}')
#         attenuation_factor_signal.set(att_fact_selected[f'att{atten_2}'])
#         newvalue = (value) * attenuation_factor_signal.get()
#         # print(newvalue)
#         self.corrected_signal.set(newvalue)



# # quadem = new_qm("XF:11BMB-BI{IM:3}:IC2_MON", name="quadem")
# # quadem = new_qm("XF:11BMB-BI{IM:3}:IC", name="quadem")
# quadem = QuadEMV33("XF:11BMB-BI{IM:3}:IC2_MON", name="quadem")
# quadem.conf.port_name.put("EM180")
# quadem.stage_sigs["acquire_mode"] = 2


# for i in [1, 2, 3, 4]:
#     getattr(quadem, f"{i}_MON").mean_value.kind = "normal"

# # for i in [1,2,3]:
# # for i in [2,3]:
# #     getattr(quadem, f"current{i}").mean_value.kind = "hinted"

    
# quadem.integration_time.put(0.0004)
# quadem.values_per_read.put(500)
# #for continuous reading
# quadem.acquire_mode.put(2)
# #for diamond mode
# quadem.geometry.put(0)


# quadem1_cl = EpicsSignal("XF:12ID1-BI{EM:1}EM1:ComputeCurrentOffset1.PROC", name="quadem1_clear")
# quadem2_cl = EpicsSignal("XF:12ID1-BI{EM:1}EM1:ComputeCurrentOffset2.PROC", name="quadem2_clear")
# quadem3_cl = EpicsSignal("XF:12ID1-BI{EM:1}EM1:ComputeCurrentOffset3.PROC", name="quadem3_clear")

from datetime import datetime, timezone
from typing import Any, Dict, TypeVar
A, B = TypeVar("A"), TypeVar("B")

class OrderedDictType(Dict[A, B]):
    ...

def quadem_clear():
    yield from bps.mv(quadem1_cl,1)
    yield from bps.mv(quadem2_cl,1)
    yield from bps.mv(quadem3_cl,1)


class IonChamber(Device):
    """
    IonChamber is operated by Oxford 400, including 4 channels. 
    ch4 is used independently on the beam intensity monitoring at s4. 
    """
    ch1 = Cpt(EpicsSignal, 'IC1_MON')
    ch2 = Cpt(EpicsSignal, 'IC2_MON')
    ch3 = Cpt(EpicsSignal, 'IC3_MON')
    ch4 = Cpt(EpicsSignal, 'IC4_MON')
    period_setpoint = Cpt(EpicsSignal, 'PERIOD_SP')
    period_readback = Cpt(EpicsSignal, 'PERIOD_MON')
    # period_readback = Cpt(EpicsSignal, 'ITIME_MON')
    count = Cpt(EpicsSignal, 'GETCS')

    def setExposureTime(self, exptime,**kwargs):
        while self.period_readback.get() != exptime:
            time.sleep(0.1)
            self.period_setpoint.set(exptime)
        print("Set Ion Chamber exposure time to {} s".format(self.period_readback.get()))
        # return time

    # from bluesky.plan_stubs import trigger_and_read

    def read(self) -> OrderedDictType[str, Dict[str, Any]]:

        # print("Triggering Ion Chamber...")
        self.count.put(0)

        # print("Reading Ion Chamber...")
        time.sleep(self.period_readback.get()+0.1)
        # print(f"Exposed {self.period_readback.get()} s")

        now = datetime.now(timezone.utc).timestamp()
        
        return {
            # f"{self.name}_ch_all": {
            #     'value': np.log10(self.ch1.get()/2+self.ch2.get()/2),
            #     'timestamp': now
            # },
            f"{self.name}_ch4": {
                'value': np.log10(self.ch4.get()),
                'timestamp': now
            },
            f"{self.name}_ch3": {
                'value': np.log10(self.ch3.get()),
                'timestamp': now
            },
            f"{self.name}_ch2": {
                'value': np.log10(abs(self.ch2.get())),
                'timestamp': now
            },
            f"{self.name}_ch1": {
                'value': np.log10(self.ch1.get()),
                'timestamp': now
            },
            f"{self.name}_period_setpoint": {
                'value': self.period_setpoint.get(),
                'timestamp': now
            },
            f"{self.name}_period_readback": {
                'value': self.period_readback.get(),
                'timestamp': now
            },
            f"{self.name}_count": {
                'value': self.count.get(),
                'timestamp': now
            }
        }

    def trigger_and_read(self):
        # return self.count.get()
        print("Triggering Ion Chamber...")
        yield from bps.mv(self.count,1) 
        # return self.ch4.get()   
        
    def expose(self, monitor_type='all'):
        # return self.count.get()
        RE(bps.mv(self.count,1)) 

        if monitor_type=='ch4':
            return self.ch4.get()   
        elif monitor_type=='ch1':
            return self.ch1.get()
        elif monitor_type=='ch2':
            return self.ch2.get()
        elif monitor_type=='ch3':
            return self.ch3.get()
        elif monitor_type=='all':
            return (self.ch1.get()+self.ch2.get())/2
        

    # def setExposureTime(self, time):
    #     self.period_setpoint.ut(time)
    #     print("Set Ion Chamber exposure time to {} s".format(self.period_readback.get()))


    # ch2 = Cpt(EpicsSignal, 'Current2:MeanValue_RBV')
    # ch3 = Cpt(EpicsSignal, 'Current3:MeanValue_RBV')
    # ch4 = Cpt(EpicsSignal, 'Current4:MeanValue_RBV')
    # sumX = Cpt(EpicsSignal, 'SumX:MeanValue_RBV')
    # sumY = Cpt(EpicsSignal, 'SumY:MeanValue_RBV')
    # posX = Cpt(EpicsSignal, 'PosX:MeanValue_RBV')
    # posY = Cpt(EpicsSignal, 'PosY:MeanValue_RBV')


#ben commented this out on 9/20/21 due to errors
ic = IonChamber("XF:11BMB-BI{IM:3}:", name="ic")


# bpm.ch1.kind = 'hinted'
# bpm.ch2.kind = 'hinted'
# bpm.ch3.kind = 'hinted'
ic.ch1.kind = 'hinted'
ic.ch2.kind = 'hinted'
# ic.ch4.kind = 'hinted'

# bpm.sumX.kind = 'hinted'
# bpm.sumY.kind = 'hinted'
# bpm.posX.kind = 'normal'
# bpm.posY.kind = 'normal'

