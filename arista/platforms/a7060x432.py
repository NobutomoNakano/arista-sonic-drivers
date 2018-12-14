from ..core.component import Priority
from ..core.driver import KernelDriver
from ..core.platform import registerPlatform, Platform
from ..core.types import NamedGpio, PciAddr, ResetGpio
from ..core.utils import incrange

from ..components.common import I2cKernelComponent, SwitchChip
from ..components.dpm import Ucd90320, UcdGpi
from ..components.scd import Scd

@registerPlatform('DCS-7060PX4-32')
class BlackhawkO(Platform):
   def __init__(self):
      super(BlackhawkO, self).__init__()

      self.qsfpRange = incrange(1, 32)
      self.sfpRange = incrange(33, 34)

      self.inventory.addPorts(qsfps=self.qsfpRange, sfps=self.sfpRange)

      self.addDriver(KernelDriver, 'rook-fan-cpld')
      self.addDriver(KernelDriver, 'rook-led-driver')

      switchChip = SwitchChip(PciAddr(bus=0x06))
      self.addComponent(switchChip)

      scd = Scd(PciAddr(bus=0x07))
      self.addComponent(scd)

      self.inventory.addWatchdog(scd.createWatchdog())

      scd.addComponents([
         I2cKernelComponent(scd.i2cAddr(0, 0x4d), 'max6581',
                            '/sys/class/hwmon/hwmon1'),
         I2cKernelComponent(scd.i2cAddr(3, 0x58), 'pmbus',
                            priority=Priority.BACKGROUND),
         I2cKernelComponent(scd.i2cAddr(4, 0x58), 'pmbus',
                            priority=Priority.BACKGROUND),
      ])

      scd.addSmbusMasterRange(0x8000, 8, 0x80)

      scd.addLeds([
         (0x6050, 'status'),
         (0x6060, 'fan_status'),
         (0x6070, 'psu1'),
         (0x6080, 'psu2'),
         (0x6090, 'beacon'),
      ])
      self.inventory.addStatusLeds(['status', 'fan_status', 'psu1',
         'psu2'])

      self.inventory.addResets(scd.addResets([
         ResetGpio(0x4000, 4, False, 'sat_cpld1_reset'),
         ResetGpio(0x4000, 3, False, 'sat_cpld0_reset'),
         ResetGpio(0x4000, 2, False, 'switch_chip_reset'),
         ResetGpio(0x4000, 0, False, 'security_asic_reset'),
      ]))

      scd.addGpios([
         NamedGpio(0x5000, 0, True, False, "psu2_present"),
         NamedGpio(0x5000, 1, True, False, "psu1_present"),
         NamedGpio(0x5000, 8, True, False, "psu2_status"),
         NamedGpio(0x5000, 9, True, False, "psu1_status"),
         NamedGpio(0x5000, 10, True, False, "psu2_ac_status"),
         NamedGpio(0x5000, 11, True, False, "psu1_ac_status"),
      ])
      self.inventory.addPsus([
         scd.createPsu(1),
         scd.createPsu(2),
      ])

      addr = 0x6100
      for xcvrId in self.qsfpRange:
         name = "qsfp%d" % xcvrId
         scd.addLed(addr, name)
         self.inventory.addXcvrLed(xcvrId, name)
         addr += 0x40

      addr = 0x6900
      for xcvrId in self.sfpRange:
         name = "sfp%d" % xcvrId
         scd.addLed(addr, name)
         self.inventory.addXcvrLed(xcvrId, name)
         addr += 0x40

      intrRegs = [
         scd.createInterrupt(addr=0x3000, num=0),
         scd.createInterrupt(addr=0x3030, num=1),
         scd.createInterrupt(addr=0x3060, num=2),
      ]

      addr = 0xA010
      bus = 8
      for xcvrId in sorted(self.qsfpRange):
         intr = intrRegs[1].getInterruptBit(xcvrId - 1)
         self.inventory.addInterrupt('qsfp%d' % xcvrId, intr)
         xcvr = scd.addQsfp(addr, xcvrId, bus, interruptLine=intr)
         self.inventory.addXcvr(xcvr)
         addr += 0x10
         bus += 1

      addr = 0xA210
      bus = 40
      for xcvrId in sorted(self.sfpRange):
         xcvr = scd.addSfp(addr, xcvrId, bus)
         self.inventory.addXcvr(xcvr)
         addr += 0x10
         bus += 1

      cpld = Scd(PciAddr(bus=0xff, device=0x0b, func=3))
      self.addComponent(cpld)

      cpld.addSmbusMasterRange(0x8000, 4, 0x80, 4)
      cpld.addComponents([
         I2cKernelComponent(cpld.i2cAddr(0, 0x4d), 'max6581'),
         Ucd90320(cpld.i2cAddr(10, 0x34), priority=Priority.BACKGROUND, causes={
            'overtemp': UcdGpi(1),
            'powerloss': UcdGpi(3),
            'watchdog': UcdGpi(5),
            'reboot': UcdGpi(7),
         }),
         I2cKernelComponent(cpld.i2cAddr(12, 0x60), 'rook_cpld',
                            '/sys/class/hwmon/hwmon2'),
         I2cKernelComponent(cpld.i2cAddr(15, 0x20), 'rook_leds'),
         I2cKernelComponent(cpld.i2cAddr(15, 0x48), 'lm73'),
      ])

      self.inventory.addPowerCycle(cpld.createPowerCycle())

@registerPlatform('DCS-7060DX4-32')
class BlackhawkDD(BlackhawkO):
   pass
