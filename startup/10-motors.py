print(f'Loading {__file__}')

from ophyd import EpicsMotor, Device, Component as Cpt

# slity = EpicsMotor('XF:11BMA-OP{Slt:0-Ax:T}Mtr', name='slity')


# class Slits(Device):
#    top = Cpt(EpicsMotor, '-Ax:T}Mtr')
#    bottom = Cpt(EpicsMotor, '-Ax:B}Mtr')

beamline_stage = "default"  #for AB, please also change Smpl2-Y from 3... to -5 
#beamline_stage = 'open_MAXS'
# beamline_stage = 'BigHuber'

print('Beamline_stage = {}'.format(beamline_stage))

# slits = Slits('XF:11BMA-OP{Slt:0', name='slits')

###################################################################################
# above as found on 19 Oct 2016, then commented out
# below added by MF in Oct 2016
###################################################################################


########## motor classes ##########
class MotorCenterAndGap(Device):
    "Center and gap using Epics Motor records"
    xc = Cpt(EpicsMotor, "-Ax:XC}Mtr")
    yc = Cpt(EpicsMotor, "-Ax:YC}Mtr")
    xg = Cpt(EpicsMotor, "-Ax:XG}Mtr")
    yg = Cpt(EpicsMotor, "-Ax:YG}Mtr")


class Blades(Device):
    "Actual T/B/O/I and virtual center/gap using Epics Motor records"
    tp = Cpt(EpicsMotor, "-Ax:T}Mtr")
    bt = Cpt(EpicsMotor, "-Ax:B}Mtr")
    ob = Cpt(EpicsMotor, "-Ax:O}Mtr")
    ib = Cpt(EpicsMotor, "-Ax:I}Mtr")
    xc = Cpt(EpicsMotor, "-Ax:XCtr}Mtr")
    yc = Cpt(EpicsMotor, "-Ax:YCtr}Mtr")
    xg = Cpt(EpicsMotor, "-Ax:XGap}Mtr")
    yg = Cpt(EpicsMotor, "-Ax:YGap}Mtr")


class Filter(Device):
    "Attenuator filters"
    sts = Cpt(EpicsSignal, "Pos-Sts")
    in_cmd = Cpt(EpicsSignal, "In-Cmd")
    out_cmd = Cpt(EpicsSignal, "Out-Cmd")


# class MotorSlits(Blades, MotorCenterAndGap):
#    "combine t b i o and xc yc xg yg"
#    pass

# class VirtualMotorSlits(Blades, VirtualMotorCenterAndGap):
#    "combine t b i o and xc yc xg yg"
#    pass


########## FOE motors ##########
## stages for Front End (FE) slits (divergence) (FOE)
# FE_x = EpicsMotor('FE:C11B-OP{Slt:12-Ax:X}t2.C', name='FE_x')
# FE_y = EpicsMotor('FE:C11B-OP{Slt:12-Ax:Y}t2.C', name='FE_y')


## stages for monochromator (FOE)
mono_bragg = EpicsMotor("XF:11BMA-OP{Mono:DMM-Ax:Bragg}Mtr", name="mono_bragg")
mono_pitch2 = EpicsMotor("XF:11BMA-OP{Mono:DMM-Ax:P2}Mtr", name="mono_pitch2")
mono_roll2 = EpicsMotor("XF:11BMA-OP{Mono:DMM-Ax:R2}Mtr", name="mono_roll2")
mono_perp2 = EpicsMotor("XF:11BMA-OP{Mono:DMM-Ax:Y2}Mtr", name="mono_perp2")


## stages for toroidal mirror (FOE)
mir_usx = EpicsMotor("XF:11BMA-OP{Mir:Tor-Ax:XU}Mtr", name="mir_usx")
mir_dsx = EpicsMotor("XF:11BMA-OP{Mir:Tor-Ax:XD}Mtr", name="mir_dsx")
mir_usy = EpicsMotor("XF:11BMA-OP{Mir:Tor-Ax:YU}Mtr", name="mir_usy")
mir_dsyi = EpicsMotor("XF:11BMA-OP{Mir:Tor-Ax:YDI}Mtr", name="mir_dsyi")
mir_dsyo = EpicsMotor("XF:11BMA-OP{Mir:Tor-Ax:YDO}Mtr", name="mir_dsyo")
mir_bend = EpicsMotor("XF:11BMA-OP{Mir:Tor-Ax:UB}Mtr", name="mir_bend")


########## FOE slits ##########
## FMB Oxford slits -- usage: s0.tp, s0.bt, s0.ob, s0.ib, s0.xc, s0.xg, s0.yc, s0.yg
s0 = Blades("XF:11BMA-OP{Slt:0", name="s0")


########## Endstation slits #########
## jj slits -- usage: s*.xc, s*.xg, s*.yc, s*.yg
s1 = MotorCenterAndGap("XF:11BMB-OP{Slt:1", name="s1")
s2 = MotorCenterAndGap("XF:11BMB-OP{Slt:2", name="s2")
s3 = MotorCenterAndGap("XF:11BMB-OP{Slt:3", name="s3")
s4 = MotorCenterAndGap("XF:11BMB-OP{Slt:4", name="s4")
s5 = MotorCenterAndGap("XF:11BMB-OP{Slt:5", name="s5")

# attenuators
filters = {
    f"filter{ifoil}": Filter(f"XF:11BMB-OP{{Fltr:{ifoil}}}", name=f"filter{ifoil}") for ifoil in range(1, 8 + 1)
}
# filters_sts = [fil.sts.get() for fil in filters.values()]
# filters_cmd = [fil.cmd.get() for fil in filters.values()]
# locals().update(filters)

########## Endstation motors ##########
## stages for Endstation diagnostics
bim3y = EpicsMotor("XF:11BMB-BI{IM:3-Ax:Y}Mtr", name="bim3y")
fs3y = EpicsMotor("XF:11BMB-BI{FS:3-Ax:Y}Mtr", name="fs3y")
bim4y = EpicsMotor("XF:11BMB-BI{IM:4-Ax:Y}Mtr", name="bim4y")
bim5y = EpicsMotor("XF:11BMB-BI{IM:5-Ax:Y}Mtr", name="bim5y")

## stages for sample positioning
# beamline_stage is defined by the current sample stage. 'default' is the regular vacuum chamber
#'open_WAXS' is the alternative stage position with Pilatus300k as the WAXS detector.
if beamline_stage == "default":
    smx = EpicsMotor("XF:11BMB-ES{Chm:Smpl-Ax:X}Mtr", name="smx")
    smy = EpicsMotor("XF:11BMB-ES{Chm:Smpl-Ax:Z}Mtr", name="smy")
    # 2023-Sep-12, change sth and schi back to original setting
    sth = EpicsMotor("XF:11BMB-ES{Chm:Smpl-Ax:theta}Mtr", name="sth")
    schi = EpicsMotor("XF:11BMB-ES{Chm:Smpl-Ax:chi}Mtr", name="schi")
    # 2023-Jul-29 theta not stable, switch to chi for incident angle
    # sth = EpicsMotor('XF:11BMB-ES{Chm:Smpl-Ax:chi}Mtr', name='sth')
    # schi = EpicsMotor('XF:11BMB-ES{Chm:Smpl-Ax:theta}Mtr', name='schi')

elif beamline_stage == "open_MAXS":
    smx = EpicsMotor("XF:11BMB-ES{Chm:Smpl2-Ax:X}Mtr", name="smx")
    smy = EpicsMotor("XF:11BMB-ES{Chm:Smpl2-Ax:Y}Mtr", name="smy")
    smz = EpicsMotor("XF:11BMB-ES{Chm:Smpl2-Ax:Z}Mtr", name="smz")
    # sth = EpicsMotor('XF:11BMB-ES{SM:2-Ax:theta}Mtr', name='sth')
    # schi = EpicsMotor('XF:11BMB-ES{SM:2-Ax:chi}Mtr', name='schi')
    # swap sth and schi at 082219 by RL
    sth = EpicsMotor("XF:11BMB-ES{SM:2-Ax:theta}Mtr", name="sth")
    schi = EpicsMotor("XF:11BMB-ES{SM:2-Ax:chi}Mtr", name="schi")

elif beamline_stage == "BigHuber":
    # Huber
    smy = EpicsMotor("XF:11BMB-ES{Chm:Smpl3-Ax:Y}Mtr", name="smy")
    sth = EpicsMotor("XF:11BMB-ES{Chm:Smpl3-Ax:theta}Mtr", name="sth")
    schi = EpicsMotor("XF:11BMB-ES{Chm:Smpl3-Ax:chi}Mtr", name="schi")

    # # Newports for PTA
    # smx = EpicsMotor('XF:11BMB-ES{PTA:Sample-Ax:X}Mtr', name='smx')
    # laserx = EpicsMotor('XF:11BMB-ES{PTA:Laser-Ax:X}Mtr', name='laserx')
    # lasery = EpicsMotor('XF:11BMB-ES{PTA:Laser-Ax:Y}Mtr', name='lasery')

    # # # GDoerk's spray coater
    smx = EpicsMotor("XF:11BMB-ES{Chm:Smpl2-Ax:Y}Mtr", name="smx")
    # # smx = EpicsMotor('XF:11BMB-ES{ESP:3-Ax:C1}Mtr', name='smx')
    sprayy = EpicsMotor("XF:11BMB-ES{Chm:Smpl2-Ax:X}Mtr", name="sprayy")


# goniometer
smy2 = EpicsMotor("XF:11BMB-ES{Chm:Smpl-Ax:Y}Mtr", name="smy2")
sphi = EpicsMotor("XF:11BMB-ES{Chm:Smpl-Ax:phi}Mtr", name="sphi")


srot = EpicsMotor("XF:11BMB-ES{SM:1-Ax:Srot}Mtr", name="srot")
strans = EpicsMotor("XF:11BMB-ES{SM:1-Ax:Strans}Mtr", name="strans")
strans2 = EpicsMotor("XF:11BMB-ES{SM:1-Ax:Strans2}Mtr", name="strans2")
stilt = EpicsMotor("XF:11BMB-ES{SM:1-Ax:Stilt}Mtr", name="stilt")
stilt2 = EpicsMotor("XF:11BMB-ES{SM:1-Ax:Stilt2}Mtr", name="stilt2")

# the srot is fixed after repair but two module controllers are broken,
# strans, strans2, stilt, stilt2 and strot are moved to backup controllers
# changed by RL 20220727
# strans =  EpicsMotor('XF:11BMB-ES{Spare:L-Ax:M}Mtr', name='strans')
# strans2 = EpicsMotor('XF:11BMB-ES{Spare:L-Ax:2}Mtr', name='strans2')
# stilt = EpicsMotor('XF:11BMB-ES{Spare:L-Ax:0}Mtr', name='stilt')
# stilt2 = EpicsMotor('XF:11BMB-ES{Spare:L-Ax:1}Mtr', name='stilt2')
# srot = EpicsMotor('XF:11BMB-ES{Spare:L-Ax:L}Mtr', name='srot')

# srot = None
# strans = None
# strans2 = None
# stilt = None
# stilt2 = None

## stages for on-axis sample camera mirror/lens
camx = EpicsMotor("XF:11BMB-ES{Cam:OnAxis-Ax:X1}Mtr", name="camx")
camy = EpicsMotor("XF:11BMB-ES{Cam:OnAxis-Ax:Y1}Mtr", name="camy")

## stages for off-axis sample camera
cam2x = EpicsMotor("XF:11BMB-ES{Cam:OnAxis-Ax:X2}Mtr", name="cam2x")
cam2z = EpicsMotor("XF:11BMB-ES{Cam:OnAxis-Ax:Y2}Mtr", name="cam2z")

## stages for sample exchanger
armz = EpicsMotor("XF:11BMB-ES{SM:1-Ax:Z}Mtr", name="armz")
armx = EpicsMotor("XF:11BMB-ES{SM:1-Ax:X}Mtr", name="armx")
armphi = EpicsMotor("XF:11BMB-ES{SM:1-Ax:Yaw}Mtr", name="armphi")
army = EpicsMotor("XF:11BMB-ES{SM:1-Ax:Y}Mtr", name="army")
# armr = EpicsMotor('XF:11BMB-ES{SM:1-Ax:ArmR}Mtr', name='armr')

# The SmarAct module is broken. Need to change to a SPARE_S for armr
# changed from spareM to spareS by RL at 2021/07/23
# armr = EpicsMotor("XF:11BMB-ES{Spare:L-Ax:S}Mtr", name="armr")
# changed to camy2 as armr was not integrated into MCS2 at 2025/04/02
# armr = EpicsMotor("XF:11BMB-ES{Cam:OnAxis-Ax:Y2}Mtr", name="armr")
armr = EpicsMotor("XF:11BMB-ES{ATT:1-Ax:X}Mtr", name="armr")


## stages for detectors
## currently not working. The new pilatus800k is sitting on a stage with manual movement
# DETx = EpicsMotor('XF:11BMB-ES{Det:Stg-Ax:X}Mtr', name='DETx')
# DETy =  EpicsMotor('XF:11BMB-ES{Det:Stg-Ax:Y}Mtr', name='DETy')
# WAXSx = EpicsMotor('XF:11BMB-ES{Det:WAXS-Ax:X}Mtr', name='WAXSx')
WAXSx = EpicsMotor("XF:11BMB-ES{Det:WAXS-Ax:X}Mtr", name="WAXSx")
WAXSy = EpicsMotor("XF:11BMB-ES{Det:WAXS-Ax:Y}Mtr", name="WAXSy")
WAXSz = EpicsMotor("XF:11BMB-ES{Det:WAXS-Ax:Z}Mtr", name="WAXSz")

SAXSx = EpicsMotor("XF:11BMB-ES{Det:SAXS-Ax:X}Mtr", name="SAXSx")
SAXSy = EpicsMotor("XF:11BMB-ES{Det:SAXS-Ax:Y}Mtr", name="SAXSy")

MAXSx = EpicsMotor("XF:11BMB-ES{Det:MAXS-Ax:X}Mtr", name="MAXSx")
MAXSy = EpicsMotor("XF:11BMB-ES{Det:MAXS-Ax:Y}Mtr", name="MAXSy")

## stages for beamstops
# bsx = EpicsMotor('XF:11BMB-ES{BS:SAXS-Ax:X}Mtr', name='bsx')
# bsy = EpicsMotor('XF:11BMB-ES{BS:SAXS-Ax:Y}Mtr', name='bsy')
# bsphi = EpicsMotor('XF:11BMB-ES{BS:SAXS-Ax:phi}Mtr', name='bsphi')

# beamstop in SmarAct MCS2 controller --- MCS11 --01/18/24
bsx = EpicsMotor("XF:11BMB-ES{BS-Ax:X}Mtr", name="bsx")
bsy = EpicsMotor("XF:11BMB-ES{BS-Ax:Y}Mtr", name="bsy")
bsphi = EpicsMotor("XF:11BMB-ES{BS-Ax:Phi}Mtr", name="bsphi")

# bsx = EpicsMotor("XF:11BMB-ES{Spare:L-Ax:S}Mtr", name="bsx")
# bsy = EpicsMotor("XF:11BMB-ES{Spare:L-Ax:L}Mtr", name="bsy")
# bsphi = EpicsMotor("XF:11BMB-ES{Spare:L-Ax:M}Mtr", name="bsphi")

##stage for vacuum gate
gatex = EpicsMotor("XF:11BMB-ES{Chm:Gate-Ax:X}Mtr", name="gatex")


# Modular Table --- MC07 --10/01/24

TABLEr = EpicsMotor("XF:11BMB-ES{Tbl:Rear-Ax:Z}Mtr", name="TABLEr")
TABLEn = EpicsMotor("XF:11BMB-ES{Tbl:Near-Ax:Z}Mtr", name="TABLEn")
TABLEd = EpicsMotor("XF:11BMB-ES{Tbl:End-Ax:Z}Mtr", name="TABLEd")

# For MDrive (X, Y, edited by YZ, 20230920)
#mdx = EpicsMotor("XF:11BM-ES{Mdrive-Ax:X}Mtr", name="mdx")
#mdy = EpicsMotor("XF:11BM-ES{Mdrive-Ax:Y}Mtr", name="mdy")

# mdx = EpicsMotor("XF:11BM-ES{Mdrive-Ax:6}Mtr", name="mdx")
# mdy = EpicsMotor("XF:11BM-ES{Mdrive-Ax:1}Mtr", name="mdy")


## easy access for stages
def wbs():
    print("bsx = {}".format(bsx.position))
    print("bsy = {}".format(bsy.position))
    print("bsphi = {}".format(bsphi.position))


def wsam():
    print("smx = {}".format(smx.position))
    print("smy = {}".format(smy.position))
    print("sth = {}".format(sth.position))


def wWAXS():
    print("WAXSx = {}".format(WAXSx.position))
    print("WAXSy = {}".format(WAXSy.position))
    print("WAXSz = {}".format(WAXSz.position))


def wSAXS():
    print("SAXSx = {}".format(SAXSx.position))
    print("SAXSy = {}".format(SAXSy.position))


def wMAXS():
    print("MAXSx = {}".format(MAXSx.position))
    print("MAXSy = {}".format(MAXSy.position))


def wGONIO():
    print("sort = {}".format(srot.position))
    print("strans = {}".format(strans.position))
    print("strans2 = {}".format(strans2.position))
    print("stilt = {}".format(stilt.position))
    print("stilt2 = {}".format(stilt2.position))

#Add by Siyu 2025/04/14

import json
import time
from pathlib import Path
from datetime import datetime

class Beamstop:
    def __init__(self, name, config_file='beamstop_config.cfg'):
        self.name = name
        self.config_file = Path(config_file)
        self.bsx = bsx.position
        self.bsy = bsy.position
        self.bsphi = bsphi.position
        self.positions = self._load_config()
        self.load()

    @classmethod
    def get(cls, name, config_file='beamstop_config.cfg'):
        print(f"Set current beamstop to '{name}' without moving.")
        return cls(name, config_file=config_file)

    @classmethod
    def goto(cls, name, config_file='beamstop_config.cfg'):
        bs = cls(name, config_file=config_file)
        # bs._move()
        RE(bs._move())
        return bs

    def _load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.positions, f, indent=2)

    def _simulate_move(self):
        print(f"[OFFLINE] Moving motors to {self.name} position:")
        print(f"  bsx -> {self.bsx}, bsy -> {self.bsy}, bsphi -> {self.bsphi}")

    # def _move(self):
    #     print(f"Moving motors to {self.name} position:")
    #     bsx.move(0)
    #     bsy.move(0)
    #     print(f"  bsx -> {0}, bsy -> {0}")
    #     time.sleep(2)
    #     bsphi.move(self.bsphi)
    #     print(f"  bsphi -> {self.bsphi}")
    #     time.sleep(5)
    #     bsx.move(self.bsx)
    #     bsy.move(self.bsy)
    #     print(f"  bsx -> {self.bsx}, bsy -> {self.bsy}")
    #     time.sleep(2)
    #     self.show()
    #     config_update()
    #     config_load()


    def _move(self):
        print(f"Moving motors to {self.name} position:")
        yield from bps.mv(bsx, 0, bsy, 0)
        print(f"  bsx -> {0}, bsy -> {0}")
        yield from bps.mv(bsphi, self.bsphi)
        print(f"  bsphi -> {self.bsphi}")
        yield from bps.mv(bsx, self.bsx, bsy, self.bsy)
        print(f"  bsx -> {self.bsx}, bsy -> {self.bsy}")
        self.show()
        config_update()
        config_load()

    # def move(self):
    #     RE(self._move())

    def x(self):
        print(f"bsx = {self.bsx}")

    def y(self):
        print(f"bsy = {self.bsy}")

    def phi(self):
        print(f"bsphi = {self.bsphi}")

    def xr(self, delta):
        self.bsx += delta
        bsx.move(self.bsx)
        print(f"bsx moved relatively by {delta} mm -> {self.bsx}")

    def yr(self, delta):
        self.bsy += delta
        bsy.move(self.bsy)
        print(f"bsy moved relatively by {delta} mm -> {self.bsy}")

    def phir(self, delta):
        self.bsphi += delta
        bsphi.move(self.bsphi)
        print(f"bsphi moved relatively by {delta} deg -> {self.bsphi}")

    def xabs(self, value):
        self.bsx = value
        bsx.move(self.bsx)
        print(f"bsx moved to {value} mm")

    def yabs(self, value):
        self.bsy = value
        bsy.move(self.bsy)
        print(f"bsy moved to {value} mm")

    def phiabs(self, value):
        self.bsphi = value
        bsphi.move(self.bsphi)
        print(f"bsphi moved to {value} deg")

    def save(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            'bsx': self.bsx,
            'bsy': self.bsy,
            'bsphi': self.bsphi,
            'timestamp': timestamp
        }
        self.positions.setdefault(self.name, []).append(entry)
        self._save_config()
        print(f"Saved current position for '{self.name}' at {timestamp}.")

    def load(self):
        entries = self.positions.get(self.name)
        if entries:
            latest = entries[-1]
            self.bsx = latest['bsx']
            self.bsy = latest['bsy']
            self.bsphi = latest['bsphi']
            print(f"Loaded last position for '{self.name}' from {latest.get('timestamp', 'unknown')}")
        else:
            print(f"No saved position found for '{self.name}'.")

    def show(self):
        print(f"Beamstop '{self.name}':")
        print(f"  bsx = {self.bsx}")
        print(f"  bsy = {self.bsy}")
        print(f"  bsphi = {self.bsphi}")

    @staticmethod
    def clear_cfg(config_file='beamstop_config.cfg'):
        path = Path(config_file)
        if path.exists():
            with open(path, 'r') as f:
                data = json.load(f)
            for key in data:
                if isinstance(data[key], list) and len(data[key]) > 0:
                    data[key] = [data[key][-1]]
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            print("Configuration file cleaned: only latest entries retained.")
        else:
            print("Config file does not exist.")