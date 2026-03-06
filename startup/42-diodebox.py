# XF:11BMB-CT{DIODE-Local:3}OutCh00:Data-SP

# PV list of Diode box: AO, Analog Output
# class Diode_AIpv(object):
# def __init__(self, ii):
# self.name = 'AI_Chan{}'.format(ii)
# self.sts = 'XF:11BMB-ES{}AI:{}-I'.format('{IO}', ii)
# Diode_AI=[None]
# for ii in range(1, 9):
# Diode_AI.append(AIpv(ii))


Diode_AO = EpicsSignal("XF:11BMB-CT{DIODE-Local:3}OutCh00:Data-SP")
Diode_A1 = EpicsSignal("XF:11BMB-CT{DIODE-Local:3}OutCh01:Data-SP")
Diode_A2 = EpicsSignal("XF:11BMB-CT{DIODE-Local:3}OutCh02:Data-SP")
Diode_A3 = EpicsSignal("XF:11BMB-CT{DIODE-Local:3}OutCh03:Data-SP")
# caput('XF:11BMB-CT{DIODE-Local:3}OutCh00:Data-SP.DESC', 'Diode AO 1')
# Diode_AO.get()
# Diode_AO.set()



class DiodeBox(Device):
    """
    DiodeBox has 4 channels
    The mode, unit and limits need to be configured in the EPICS.
    2026-02-18
    """
    # Setpoint, using set() or put()
    A0_SP = Cpt(EpicsSignal, 'OutCh00:Data-SP')
    A1_SP = Cpt(EpicsSignal, 'OutCh01:Data-SP')
    A2_SP = Cpt(EpicsSignal, 'OutCh02:Data-SP')
    A3_SP = Cpt(EpicsSignal, 'OutCh03:Data-SP')

    # Readback, using get()
    A0_RB = Cpt(EpicsSignal, 'InCh00:Data-RB')
    A1_RB = Cpt(EpicsSignal, 'InCh01:Data-RB')
    A2_RB = Cpt(EpicsSignal, 'InCh02:Data-RB')
    A3_RB = Cpt(EpicsSignal, 'InCh03:Data-RB')



    def set(self, channel=0, setpoint=0):
        '''set a target value to a target channel'''
        Ch_SP = getattr(self, f'A{channel}_SP')
        Ch_SP.set(setpoint)
        print(f'{self.name}: Channel {channel} is set to {setpoint}.')


    def get(self, channel=0):
        '''get a RB value for a target channel'''
        Ch_RB = getattr(self, f'A{channel}_RB')
        rb = Ch_RB.get()
        print(f'{self.name}: Channel {channel} is {rb}.')
        return rb


    def set_and_waitRB(self, channel=0, setpoint=0):
        '''set a target value to a target channel and wait for the readback'''

        Ch_SP = getattr(self, f'A{channel}_SP')
        Ch_RB = getattr(self, f'A{channel}_RB')
        
        Ch_SP.set(setpoint)
        start_time = time.time()
        while abs(Ch_RB.get()-setpoint) > 0.001:
            time.sleep(0.05)
        print(f'Time elapse = {time.time()-start_time: .4f}s')
        print(f'{self.name}: Channel {channel} is set to {setpoint}.')


diodebox3 = DiodeBox("XF:11BMB-CT{DIODE-Local:3}", name="Diodebox3")